/**
 * Twitter/X Bookmark Folder Extractor v3
 *
 * Two modes:
 *   Mode A (Claude-in-Chrome): Execute via mcp__claude-in-chrome__javascript_tool
 *     - Auth comes from document.cookie (CSRF) + standard bearer token
 *     - Hash/features can be passed as parameters for self-healing
 *     - Call: fetchBookmarkFolder("FOLDER_ID", { hash, features })
 *
 *   Mode B (Manual DevTools): Copy cURL from Network tab
 *     - Run: setAuthFromCurl(`paste_here`)
 *     - Run: await fetchBookmarkFolder("FOLDER_ID")
 *
 * PAGINATION: Full-scan-and-dedup. The bookmark folder ordering is randomized
 * (not chronological), so we fetch ALL pages and let the caller deduplicate
 * against the DB. There is no stop-at-known-ID logic.
 *
 * HASH SELF-HEALING: The GraphQL hash changes on every Twitter deploy. Rather
 * than hardcoding, capture the live BookmarkFolderTimeline request from the
 * network tab and pass the hash/features as parameters. The DEFAULT_HASH below
 * is a fallback for when no live capture is available.
 *
 * Updated: 2026-02-12
 */

// --- Defaults (fallback when no live capture is provided) ---

const DEFAULT_HASH = 'LdT6YZk9yx_o1xbLN61epw';

const DEFAULT_FEATURES = {
  rweb_video_screen_enabled: false,
  profile_label_improvements_pcf_label_in_post_enabled: true,
  responsive_web_profile_redirect_enabled: false,
  rweb_tipjar_consumption_enabled: false,
  verified_phone_label_enabled: false,
  creator_subscriptions_tweet_preview_api_enabled: true,
  responsive_web_graphql_timeline_navigation_enabled: true,
  responsive_web_graphql_skip_user_profile_image_extensions_enabled: false,
  premium_content_api_read_enabled: false,
  communities_web_enable_tweet_community_results_fetch: true,
  c9s_tweet_anatomy_moderator_badge_enabled: true,
  responsive_web_grok_analyze_button_fetch_trends_enabled: false,
  responsive_web_grok_analyze_post_followups_enabled: true,
  responsive_web_jetfuel_frame: true,
  responsive_web_grok_share_attachment_enabled: true,
  responsive_web_grok_annotations_enabled: true,
  articles_preview_enabled: true,
  responsive_web_edit_tweet_api_enabled: true,
  graphql_is_translatable_rweb_tweet_is_translatable_enabled: true,
  view_counts_everywhere_api_enabled: true,
  longform_notetweets_consumption_enabled: true,
  responsive_web_twitter_article_tweet_consumption_enabled: true,
  tweet_awards_web_tipping_enabled: false,
  responsive_web_grok_show_grok_translated_post: true,
  responsive_web_grok_analysis_button_from_backend: true,
  post_ctas_fetch_enabled: true,
  freedom_of_speech_not_reach_fetch_enabled: true,
  standardized_nudges_misinfo: true,
  tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled: true,
  longform_notetweets_rich_text_read_enabled: true,
  longform_notetweets_inline_media_enabled: true,
  responsive_web_grok_image_annotation_enabled: true,
  responsive_web_grok_imagine_annotation_enabled: true,
  responsive_web_grok_community_note_auto_translation_is_enabled: false,
  responsive_web_enhance_cards_enabled: false
};

const BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA';

// --- Auth ---

let capturedAuth = null;

/**
 * Mode A auth: Build headers from page context (Claude-in-Chrome).
 * Call this when running inside x.com via javascript_tool.
 */
function setAuthFromPage() {
  const csrfToken = document.cookie.split('; ')
    .find(c => c.startsWith('ct0='))
    ?.split('=')[1];

  if (!csrfToken) {
    console.error('No ct0 cookie found — are you on x.com?');
    return false;
  }

  capturedAuth = {
    'authorization': BEARER_TOKEN,
    'x-csrf-token': csrfToken,
    'content-type': 'application/json',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en'
  };
  console.log('Auth set from page cookies');
  return true;
}

/**
 * Mode B auth: Extract headers from a cURL command (manual DevTools).
 */
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
    console.error('No x-csrf-token found in cURL');
    return false;
  }

  capturedAuth = {
    'authorization': headers['authorization'] || BEARER_TOKEN,
    'x-csrf-token': csrfToken,
    'cookie': headers['cookie'] || document.cookie,
    'content-type': 'application/json',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en'
  };
  console.log('Auth set from cURL');
  return true;
}

// --- Tweet parsing ---

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

    const media = (legacy.extended_entities?.media || []).map(m => ({
      type: m.type,
      url: m.media_url_https,
      expanded_url: m.expanded_url,
      alt_text: m.ext_alt_text || null,
      video_url: m.video_info?.variants?.find(v => v.content_type === 'video/mp4')?.url || null
    }));

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

// --- Main fetch ---

let allBookmarks = [];

/**
 * Fetch all bookmarks from a folder. Full-scan pagination (no early stop).
 *
 * @param {string} folderId - The bookmark folder ID
 * @param {object} options
 * @param {string} options.hash - GraphQL query hash (override DEFAULT_HASH)
 * @param {object} options.features - Features object (override DEFAULT_FEATURES)
 * @param {number} options.delay - Delay between pages in ms (default: 1500)
 * @param {number} options.maxPages - Safety limit (default: 50)
 * @param {boolean} options.fetchReplies - Also fetch reply threads (default: false)
 * @param {number} options.replyThreshold - Min replies to fetch thread (default: 10)
 */
async function fetchBookmarkFolder(folderId, options = {}) {
  const hash = options.hash || DEFAULT_HASH;
  const features = options.features || DEFAULT_FEATURES;
  const delay = options.delay || 1500;
  const maxPages = options.maxPages || 50;
  const fetchReplies = options.fetchReplies || false;
  const replyThreshold = options.replyThreshold || 10;

  // Auto-set auth from page cookies if not already set (Mode A)
  if (!capturedAuth) {
    if (typeof document !== 'undefined' && document.cookie.includes('ct0=')) {
      setAuthFromPage();
    } else {
      console.error('No auth — run setAuthFromPage() or setAuthFromCurl() first');
      return [];
    }
  }

  allBookmarks = [];
  const seenIds = new Set();

  const baseVars = {
    bookmark_collection_id: folderId,
    includePromotedContent: true
    // NO count parameter — Twitter rejects it
  };

  console.log('Bookmark Folder Extractor v3 — full-scan mode');
  console.log('Hash:', hash);

  let cursor = null;
  let page = 0;

  while (page < maxPages) {
    page++;
    const vars = cursor ? { ...baseVars, cursor } : baseVars;

    const url = `https://x.com/i/api/graphql/${hash}/BookmarkFolderTimeline` +
      '?variables=' + encodeURIComponent(JSON.stringify(vars)) +
      '&features=' + encodeURIComponent(JSON.stringify(features));

    console.log(`Page ${page}...`);

    try {
      const res = await fetch(url, { headers: capturedAuth, credentials: 'include' });

      if (!res.ok) {
        const txt = await res.text();
        console.error(`HTTP ${res.status}: ${txt.substring(0, 200)}`);
        if (res.status === 400) {
          console.error('Hash may be stale — capture a fresh one from network requests');
        }
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

      console.log(`  ${count} tweets (total: ${allBookmarks.length})`);

      if (!nextCursor) {
        console.log('End of folder');
        break;
      }

      cursor = nextCursor;
      await new Promise(r => setTimeout(r, delay));

    } catch (e) {
      console.error('Fetch error:', e.message);
      break;
    }
  }

  // Fetch replies if requested
  if (fetchReplies && allBookmarks.length > 0) {
    const highEngagement = allBookmarks.filter(b => b.metrics.replies > replyThreshold);
    console.log(`Fetching replies for ${highEngagement.length} high-engagement tweets...`);

    for (const b of highEngagement) {
      try {
        b.replies = await fetchTweetReplies(b.id, { hash, features });
        console.log(`  ${b.author.handle}: ${b.replies.length} replies`);
      } catch (e) {
        console.error(`  Reply fetch failed: ${e.message}`);
        b.replies = [];
      }
      await new Promise(r => setTimeout(r, delay));
    }
  }

  window._fetchedBookmarks = allBookmarks;
  window.bookmarks = allBookmarks;

  console.log(`Complete: ${allBookmarks.length} bookmarks`);
  console.log(`  With media: ${allBookmarks.filter(b => b.media.length > 0).length}`);
  console.log(`  With cards: ${allBookmarks.filter(b => b.card).length}`);

  return allBookmarks;
}

// --- Reply fetching ---

async function fetchTweetReplies(tweetId, options = {}) {
  const hash = options.hash || DEFAULT_HASH;
  const features = options.features || DEFAULT_FEATURES;

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
    '&features=' + encodeURIComponent(JSON.stringify(features));

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

console.log(`Bookmark Folder Extractor v3 loaded (hash: ${DEFAULT_HASH})`);
console.log('Mode A (Claude-in-Chrome): fetchBookmarkFolder("ID", { hash, features })');
console.log('Mode B (Manual): setAuthFromCurl(\`cURL\`), then fetchBookmarkFolder("ID")');
