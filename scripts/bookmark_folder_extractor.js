/**
 * Twitter/X Bookmark Folder Extractor v2
 *
 * FIXED 2026-01-02: Removed count parameter that was causing 400 errors
 * 
 * QUICK START:
 * 1. Open DevTools Network tab at your bookmark folder page
 * 2. Refresh, find "BookmarkFolderTimeline" request
 * 3. Right-click → Copy as cURL
 * 4. Run: setAuthFromCurl(`paste_here`)
 * 5. Run: await fetchBookmarkFolder("YOUR_FOLDER_ID")
 */

let capturedAuth = null;

function setAuthFromCurl(curlCommand) {
  const headerRegex = /-H\s+['"]([^:]+):\s*([^'"]+)['"]/gi;
  const headers = {};
  let match;
  while ((match = headerRegex.exec(curlCommand)) !== null) {
    headers[match[1].toLowerCase().trim()] = match[2].trim();
  }
  
  const cookieMatch = curlCommand.match(/-H\s+['"]cookie:\s*([^'"]+)['"]/i);
  if (cookieMatch) headers['cookie'] = cookieMatch[1];
  
  const csrfToken = headers['x-csrf-token'];
  if (!csrfToken) {
    console.error('❌ No x-csrf-token found');
    return false;
  }
  
  capturedAuth = {
    'authorization': headers['authorization'] || 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'x-csrf-token': csrfToken,
    'cookie': headers['cookie'] || document.cookie,
    'content-type': 'application/json',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en'
  };
  console.log('✅ Auth set');
  return true;
}

// Complete features (Twitter requires ALL of these as of Jan 2026)
const FEATURES = {
  rweb_video_screen_enabled: false,
  profile_label_improvements_pcf_label_in_post_enabled: true,
  rweb_tipjar_consumption_enabled: true,
  responsive_web_graphql_exclude_directive_enabled: true,
  verified_phone_label_enabled: false,
  creator_subscriptions_tweet_preview_api_enabled: true,
  responsive_web_graphql_timeline_navigation_enabled: true,
  responsive_web_graphql_skip_user_profile_image_extensions_enabled: false,
  communities_web_enable_tweet_community_results_fetch: true,
  c9s_tweet_anatomy_moderator_badge_enabled: true,
  articles_preview_enabled: true,
  responsive_web_edit_tweet_api_enabled: true,
  graphql_is_translatable_rweb_tweet_is_translatable_enabled: true,
  view_counts_everywhere_api_enabled: true,
  longform_notetweets_consumption_enabled: true,
  responsive_web_twitter_article_tweet_consumption_enabled: true,
  tweet_awards_web_tipping_enabled: false,
  creator_subscriptions_quote_tweet_preview_enabled: false,
  freedom_of_speech_not_reach_fetch_enabled: true,
  standardized_nudges_misinfo: true,
  tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled: true,
  rweb_video_timestamps_enabled: true,
  longform_notetweets_rich_text_read_enabled: true,
  longform_notetweets_inline_media_enabled: true,
  responsive_web_enhance_cards_enabled: false,
  // Grok features
  responsive_web_grok_community_note_auto_translation_is_enabled: false,
  responsive_web_jetfuel_frame: false,
  responsive_web_grok_show_grok_translated_post: false,
  responsive_web_profile_redirect_enabled: false,
  premium_content_api_read_enabled: false,
  responsive_web_grok_analyze_post_followups_enabled: false,
  responsive_web_grok_imagine_annotation_enabled: false,
  responsive_web_grok_analyze_button_fetch_trends_enabled: false,
  responsive_web_grok_share_attachment_enabled: false,
  responsive_web_grok_image_annotation_enabled: false,
  responsive_web_grok_analysis_button_from_backend: false
};

function parseTweet(entry) {
  try {
    const result = entry.content?.itemContent?.tweet_results?.result;
    if (!result) return null;
    
    const tweet = result.__typename === 'TweetWithVisibilityResults' ? result.tweet : result;
    if (!tweet || tweet.__typename !== 'Tweet') return null;
    
    const legacy = tweet.legacy;
    const user = tweet.core?.user_results?.result;
    const screenName = user?.core?.screen_name || user?.legacy?.screen_name || 'unknown';
    
    if (!legacy) return null;
    
    const fullText = tweet.note_tweet?.note_tweet_results?.result?.text || legacy.full_text;
    
    // Extract media with full details
    const media = (legacy.extended_entities?.media || []).map(m => ({
      type: m.type,
      url: m.media_url_https,
      expanded_url: m.expanded_url,
      alt_text: m.ext_alt_text || null,
      video_url: m.video_info?.variants?.find(v => v.content_type === 'video/mp4')?.url || null
    }));
    
    // Extract card/preview
    let card = null;
    if (tweet.card?.legacy) {
      const bindings = tweet.card.legacy.binding_values || [];
      const get = (k) => bindings.find(b => b.key === k)?.value?.string_value;
      card = { url: get('card_url'), title: get('title'), description: get('description') };
    }
    
    return {
      id: tweet.rest_id,
      text: fullText,
      author: { handle: '@' + screenName, name: user?.core?.name || '' },
      created_at: new Date(legacy.created_at).toISOString(),
      url: `https://x.com/${screenName}/status/${tweet.rest_id}`,
      metrics: {
        replies: legacy.reply_count || 0,
        retweets: legacy.retweet_count || 0,
        likes: legacy.favorite_count || 0,
        bookmarks: legacy.bookmark_count || 0,
        views: parseInt(tweet.views?.count) || 0,
        quotes: legacy.quote_count || 0
      },
      engagement_score: (legacy.favorite_count || 0) + (legacy.retweet_count || 0) * 2 + 
                        (legacy.reply_count || 0) * 3 + (legacy.bookmark_count || 0) * 2,
      conversation_id: legacy.conversation_id_str,
      is_reply: !!legacy.in_reply_to_status_id_str,
      in_reply_to: legacy.in_reply_to_status_id_str || null,
      media: media,
      card: card,
      urls: (legacy.entities?.urls || []).map(u => ({ short: u.url, expanded: u.expanded_url }))
    };
  } catch (e) {
    console.error('Parse error:', e);
    return null;
  }
}

let allBookmarks = [];

async function fetchBookmarkFolder(folderId, options = {}) {
  const delay = options.delay || 1500;
  const maxPages = options.maxPages || 20;
  const fetchReplies = options.fetchReplies || false;
  const replyThreshold = options.replyThreshold || 10;
  
  if (!capturedAuth) {
    console.error('❌ Run setAuthFromCurl() first');
    return [];
  }
  
  allBookmarks = [];
  const seenIds = new Set();
  
  // CRITICAL: Variables must NOT include "count" - Twitter rejects it
  const baseVars = {
    bookmark_collection_id: folderId,
    includePromotedContent: true
    // NO COUNT PARAMETER!
  };
  
  console.log('\n📚 Bookmark Folder Extractor v2');
  console.log('   Variables:', JSON.stringify(baseVars));
  
  let cursor = null;
  let page = 0;
  
  while (page < maxPages) {
    page++;
    const vars = cursor ? { ...baseVars, cursor } : baseVars;
    
    const url = 'https://x.com/i/api/graphql/KJIQpsvxrTfRIlbaRIySHQ/BookmarkFolderTimeline' +
      '?variables=' + encodeURIComponent(JSON.stringify(vars)) +
      '&features=' + encodeURIComponent(JSON.stringify(FEATURES));
    
    console.log(`📥 Page ${page}...`);
    
    try {
      const res = await fetch(url, { headers: capturedAuth, credentials: 'include' });
      
      if (!res.ok) {
        console.error(`❌ HTTP ${res.status}`);
        const txt = await res.text();
        console.error('Response:', txt.substring(0, 200));
        break;
      }
      
      const data = await res.json();
      const instructions = data?.data?.bookmark_collection_timeline?.timeline?.instructions || [];
      const entries = instructions.find(i => i.type === 'TimelineAddEntries')?.entries || [];
      
      let count = 0;
      let nextCursor = null;
      
      for (const entry of entries) {
        if (entry.entryId?.startsWith('cursor-bottom')) {
          nextCursor = entry.content?.value;
          continue;
        }
        if (!entry.entryId?.startsWith('tweet-')) continue;
        
        const parsed = parseTweet(entry);
        if (parsed && !seenIds.has(parsed.id)) {
          seenIds.add(parsed.id);
          allBookmarks.push(parsed);
          count++;
        }
      }
      
      console.log(`   → ${count} tweets (total: ${allBookmarks.length})`);
      
      if (!nextCursor) {
        console.log('📄 End of folder');
        break;
      }
      
      cursor = nextCursor;
      await new Promise(r => setTimeout(r, delay));
      
    } catch (e) {
      console.error('Error:', e.message);
      break;
    }
  }
  
  // Fetch replies if requested
  if (fetchReplies && allBookmarks.length > 0) {
    const highEngagement = allBookmarks.filter(b => b.metrics.replies > replyThreshold);
    console.log(`\n🔍 Fetching replies for ${highEngagement.length} high-engagement tweets...`);
    
    for (const b of highEngagement) {
      try {
        console.log(`   ${b.author.handle}: ${b.text.substring(0, 40)}...`);
        b.replies = await fetchTweetReplies(b.id);
        console.log(`   → ${b.replies.length} replies`);
      } catch (e) {
        console.error(`   ❌ ${e.message}`);
        b.replies = [];
      }
      await new Promise(r => setTimeout(r, delay));
    }
  }
  
  window.bookmarks = allBookmarks;
  
  console.log('\n════════════════════════════════════════');
  console.log(`✅ Complete: ${allBookmarks.length} bookmarks`);
  console.log('   Copy: copy(JSON.stringify(window.bookmarks, null, 2))');
  
  // Show media summary
  const withMedia = allBookmarks.filter(b => b.media.length > 0);
  const withCards = allBookmarks.filter(b => b.card);
  console.log(`   With media: ${withMedia.length}`);
  console.log(`   With cards: ${withCards.length}`);
  
  return allBookmarks;
}

async function fetchTweetReplies(tweetId) {
  const vars = {
    focalTweetId: tweetId,
    with_rux_injections: false,
    rankingMode: "Relevance",
    includePromotedContent: false,
    withCommunity: true,
    withQuickPromoteEligibilityTweetFields: true,
    withBirdwatchNotes: true,
    withVoice: true
  };
  
  const url = 'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail' +
    '?variables=' + encodeURIComponent(JSON.stringify(vars)) +
    '&features=' + encodeURIComponent(JSON.stringify(FEATURES));
  
  const res = await fetch(url, { headers: capturedAuth, credentials: 'include' });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  
  const data = await res.json();
  const replies = [];
  const seen = new Set([tweetId]);
  
  function extract(obj, depth = 0) {
    if (!obj || typeof obj !== 'object' || depth > 10) return;
    
    if (obj.__typename === 'Tweet' && obj.rest_id && !seen.has(obj.rest_id)) {
      const leg = obj.legacy;
      const user = obj.core?.user_results?.result;
      if (leg?.in_reply_to_status_id_str) {
        seen.add(obj.rest_id);
        replies.push({
          id: obj.rest_id,
          text: obj.note_tweet?.note_tweet_results?.result?.text || leg.full_text,
          author: '@' + (user?.core?.screen_name || 'unknown'),
          likes: leg.favorite_count || 0,
          in_reply_to: leg.in_reply_to_status_id_str
        });
      }
    }
    
    for (const v of Object.values(obj)) {
      if (Array.isArray(v)) v.forEach(i => extract(i, depth + 1));
      else if (typeof v === 'object') extract(v, depth + 1);
    }
  }
  
  extract(data);
  return replies.sort((a, b) => b.likes - a.likes);
}

console.log(`
╔════════════════════════════════════════════════════════════╗
║     BOOKMARK FOLDER EXTRACTOR v2 (2026-01-02)              ║
╠════════════════════════════════════════════════════════════╣
║  1. Copy cURL from Network tab (BookmarkFolderTimeline)    ║
║  2. setAuthFromCurl(\`paste_here\`)                          ║
║  3. await fetchBookmarkFolder("FOLDER_ID")                 ║
║                                                            ║
║  With replies:                                             ║
║  await fetchBookmarkFolder("ID", {                         ║
║    fetchReplies: true, replyThreshold: 5                   ║
║  })                                                        ║
╚════════════════════════════════════════════════════════════╝
`);
