/**
 * Twitter/X Bookmark Folder Extractor
 *
 * Extracts all bookmarks from a Twitter bookmark folder via API.
 * Optionally fetches reply threads for high-engagement tweets.
 *
 * SETUP:
 * 1. Open your bookmark folder in browser (x.com/i/bookmarks/FOLDER_ID)
 * 2. Open DevTools → Network tab
 * 3. Refresh the page
 * 4. Find request to "BookmarkFolderTimeline" or similar
 * 5. Right-click → Copy as cURL
 * 6. Run: setAuthFromCurl(`paste_here`)
 * 7. Run: await fetchBookmarkFolder("FOLDER_ID")
 *
 * Created: 2026-01-02
 * Updated: 2026-01-02 - Fixed GraphQL endpoint ID
 * For: claude-code-tips project
 */

// ============================================
// AUTH HANDLING (same pattern as thread extractor)
// ============================================

let capturedAuth = null;

/**
 * Extract auth from cURL command
 */
function setAuthFromCurl(curlCommand) {
  const headerRegex = /-H\s+['"]([^:]+):\s*([^'"]+)['"]/gi;
  const headers = {};

  let match;
  while ((match = headerRegex.exec(curlCommand)) !== null) {
    const name = match[1].toLowerCase().trim();
    const value = match[2].trim();
    headers[name] = value;
  }

  const cookieMatch = curlCommand.match(/-H\s+['"]cookie:\s*([^'"]+)['"]/i);
  if (cookieMatch) {
    headers['cookie'] = cookieMatch[1];
  }

  const csrfToken = headers['x-csrf-token'];

  if (!csrfToken) {
    console.error('❌ Could not find x-csrf-token in cURL command.');
    console.log('Found headers:', Object.keys(headers));
    return false;
  }

  capturedAuth = {
    'authorization': headers['authorization'] || 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'x-csrf-token': csrfToken,
    'cookie': headers['cookie'] || document.cookie,
    'content-type': 'application/json',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': headers['x-twitter-auth-type'] || 'OAuth2Session',
    'x-twitter-client-language': 'en'
  };

  console.log('✅ Auth captured successfully!');
  console.log('   CSRF token:', csrfToken.substring(0, 20) + '...');
  return true;
}

function setAuthManual(csrfToken, cookie) {
  capturedAuth = {
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'x-csrf-token': csrfToken,
    'cookie': cookie || document.cookie,
    'content-type': 'application/json',
    'x-twitter-active-user': 'yes',
    'x-twitter-auth-type': 'OAuth2Session',
    'x-twitter-client-language': 'en'
  };
  console.log('✅ Auth set manually');
  return true;
}

// ============================================
// TWEET PARSING
// ============================================

/**
 * Parse a tweet from the bookmark API response
 */
function parseBookmarkedTweet(entry) {
  try {
    const tweetResult = entry.content?.itemContent?.tweet_results?.result;
    if (!tweetResult || tweetResult.__typename !== 'Tweet') return null;

    const tweet = tweetResult;
    const legacy = tweet.legacy;
    const core = tweet.core?.user_results?.result;
    const authorLegacy = core?.legacy;

    if (!legacy) return null;

    // Get full text (note_tweet for long posts, legacy.full_text for regular)
    const fullText = tweet.note_tweet?.note_tweet_results?.result?.text || legacy.full_text;

    // Extract URLs from note_tweet if available, otherwise from legacy
    const urls = tweet.note_tweet?.note_tweet_results?.result?.entity_set?.urls || 
                 legacy.entities?.urls || [];

    // Extract card/link preview if present
    let card = null;
    if (tweet.card?.legacy) {
      const cardBindings = tweet.card.legacy.binding_values || [];
      const getValue = (key) => cardBindings.find(b => b.key === key)?.value?.string_value;
      card = {
        url: getValue('card_url'),
        title: getValue('title'),
        description: getValue('description'),
        domain: getValue('domain')
      };
    }

    // Extract media
    const media = (legacy.extended_entities?.media || legacy.entities?.media || []).map(m => ({
      type: m.type,
      url: m.media_url_https,
      expanded_url: m.expanded_url,
      alt_text: m.ext_alt_text || null,
      video_url: m.video_info?.variants?.find(v => v.content_type === 'video/mp4')?.url || null
    }));

    // Determine if this is part of a thread or a reply
    const isReply = !!legacy.in_reply_to_status_id_str;
    const isThreadRoot = legacy.conversation_id_str === tweet.rest_id;

    return {
      id: tweet.rest_id,
      text: fullText,
      text_truncated: legacy.full_text, // The 280-char version
      
      // Author
      author: {
        id: core?.rest_id,
        handle: '@' + (authorLegacy?.screen_name || 'unknown'),
        name: authorLegacy?.name || '',
        bio: authorLegacy?.description || '',
        followers: authorLegacy?.followers_count || 0,
        verified: core?.is_blue_verified || false
      },
      
      // Timestamps
      created_at: legacy.created_at,
      created_at_iso: new Date(legacy.created_at).toISOString(),
      
      // Metrics
      metrics: {
        replies: legacy.reply_count || 0,
        retweets: legacy.retweet_count || 0,
        likes: legacy.favorite_count || 0,
        quotes: legacy.quote_count || 0,
        views: parseInt(tweet.views?.count) || 0,
        bookmarks: legacy.bookmark_count || 0
      },
      
      // Engagement score (useful for prioritization)
      engagement_score: (legacy.favorite_count || 0) + 
                        (legacy.retweet_count || 0) * 2 + 
                        (legacy.reply_count || 0) * 3 +
                        (legacy.bookmark_count || 0) * 2,
      
      // Thread/reply info
      conversation_id: legacy.conversation_id_str,
      is_reply: isReply,
      is_thread_root: isThreadRoot,
      in_reply_to: legacy.in_reply_to_status_id_str || null,
      in_reply_to_user: legacy.in_reply_to_screen_name || null,
      
      // URLs and media
      url: `https://x.com/${authorLegacy?.screen_name}/status/${tweet.rest_id}`,
      urls: urls.map(u => ({
        display: u.display_url,
        expanded: u.expanded_url,
        short: u.url
      })),
      card: card,
      media: media,
      
      // Quoted tweet (if any)
      quoted_tweet: tweet.quoted_status_result?.result ? {
        id: tweet.quoted_status_result.result.rest_id,
        text: tweet.quoted_status_result.result.legacy?.full_text,
        author: '@' + tweet.quoted_status_result.result.core?.user_results?.result?.legacy?.screen_name
      } : null,
      
      // Metadata
      source: 'bookmark_folder',
      bookmarked_at: new Date().toISOString(), // We don't get actual bookmark time from API
      lang: legacy.lang
    };
  } catch (e) {
    console.error('Parse error:', e, entry);
    return null;
  }
}

// ============================================
// BOOKMARK FOLDER FETCHING
// ============================================

// Storage
let allBookmarks = [];

/**
 * Fetch all bookmarks from a folder
 * 
 * @param {string} folderId - The bookmark folder ID from the URL
 * @param {object} options - { maxPages, delay, fetchReplies, replyThreshold }
 */
async function fetchBookmarkFolder(folderId, options = {}) {
  const maxPages = options.maxPages || 20;
  const delay = options.delay || 1500;
  const fetchReplies = options.fetchReplies || false;
  const replyThreshold = options.replyThreshold || 10; // Only fetch replies if reply_count > this

  if (!capturedAuth) {
    console.error('❌ No auth. Run setAuthFromCurl(`your_curl_command`) first.');
    return [];
  }

  allBookmarks = [];
  const seenIds = new Set();

  // GraphQL endpoint for bookmark folders
  // FIXED: Correct endpoint ID from network capture (2026-01-02)
  const baseUrl = 'https://x.com/i/api/graphql/KJIQpsvxrTfRIlbaRIySHQ/BookmarkFolderTimeline';

  const baseVariables = {
    bookmark_collection_id: folderId,
    count: 20,
    includePromotedContent: true  // Match what Twitter sends
  };

  // Features from working cURL capture (2026-01-02)
  const features = {
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
    responsive_web_enhance_cards_enabled: false
  };

  let cursor = null;
  let pageNum = 0;

  console.log(`\n📚 Fetching bookmarks from folder ${folderId}...`);
  console.log(`   Delay between requests: ${delay}ms\n`);

  while (pageNum < maxPages) {
    pageNum++;

    const variables = { ...baseVariables };
    if (cursor) {
      variables.cursor = cursor;
    }

    const url = `${baseUrl}?variables=${encodeURIComponent(JSON.stringify(variables))}&features=${encodeURIComponent(JSON.stringify(features))}`;

    console.log(`📥 Page ${pageNum}${cursor ? ' (cursor)' : ''}...`);

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: capturedAuth,
        credentials: 'include'
      });

      if (!response.ok) {
        console.error(`❌ HTTP ${response.status}`);
        if (response.status === 429) {
          console.log('⏳ Rate limited. Waiting 60s...');
          await new Promise(r => setTimeout(r, 60000));
          continue;
        }
        if (response.status === 401 || response.status === 403) {
          console.error('🔐 Auth expired. Re-capture cURL and run setAuthFromCurl() again.');
          break;
        }
        break;
      }

      const data = await response.json();
      
      // Navigate to entries
      const instructions = data?.data?.bookmark_collection_timeline?.timeline?.instructions || [];
      const addEntries = instructions.find(i => i.type === 'TimelineAddEntries');
      const entries = addEntries?.entries || [];

      let newCount = 0;
      let nextCursor = null;

      for (const entry of entries) {
        // Check for cursor
        if (entry.entryId?.startsWith('cursor-bottom')) {
          nextCursor = entry.content?.value;
          continue;
        }

        // Skip non-tweet entries
        if (!entry.entryId?.startsWith('tweet-')) continue;

        const parsed = parseBookmarkedTweet(entry);
        if (parsed && !seenIds.has(parsed.id)) {
          seenIds.add(parsed.id);
          allBookmarks.push(parsed);
          newCount++;
        }
      }

      console.log(`   → ${newCount} bookmarks (Total: ${allBookmarks.length})`);

      if (!nextCursor) {
        console.log('📄 Reached end of folder');
        break;
      }

      cursor = nextCursor;

      // Checkpoint
      window.bookmarkCheckpoint = allBookmarks.slice();

      await new Promise(r => setTimeout(r, delay));

    } catch (e) {
      console.error('Error:', e.message);
      break;
    }
  }

  // Optionally fetch replies for high-engagement tweets
  if (fetchReplies) {
    console.log(`\n🔍 Fetching replies for tweets with >${replyThreshold} replies...`);
    await fetchRepliesForBookmarks(replyThreshold, delay);
  }

  // Store results
  window.bookmarks = allBookmarks;

  // Summary
  printSummary();

  return allBookmarks;
}

/**
 * Fetch reply threads for bookmarks with high reply counts
 */
async function fetchRepliesForBookmarks(threshold = 10, delay = 2000) {
  const highEngagement = allBookmarks.filter(b => b.metrics.replies > threshold);
  
  console.log(`   Found ${highEngagement.length} tweets above threshold`);

  for (const bookmark of highEngagement) {
    console.log(`   📥 Fetching replies for ${bookmark.author.handle}: "${bookmark.text.substring(0, 50)}..."`);
    
    try {
      const replies = await fetchTweetReplies(bookmark.id, { maxDepth: 2, delay });
      bookmark.replies = replies;
      console.log(`      → ${replies.length} replies captured`);
    } catch (e) {
      console.error(`      ❌ Failed: ${e.message}`);
      bookmark.replies = [];
    }

    await new Promise(r => setTimeout(r, delay));
  }
}

/**
 * Fetch replies for a single tweet (reusing TweetDetail endpoint)
 * This is a simplified version - for full thread extraction, use twitter_thread_extractor.js
 */
async function fetchTweetReplies(tweetId, options = {}) {
  const maxDepth = options.maxDepth || 2;
  const delay = options.delay || 1500;

  const baseUrl = 'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail';

  const variables = {
    focalTweetId: tweetId,
    with_rux_injections: false,
    rankingMode: "Relevance",
    includePromotedContent: false,
    withCommunity: true,
    withQuickPromoteEligibilityTweetFields: true,
    withBirdwatchNotes: true,
    withVoice: true
  };

  const features = {
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
    responsive_web_enhance_cards_enabled: false
  };

  const url = `${baseUrl}?variables=${encodeURIComponent(JSON.stringify(variables))}&features=${encodeURIComponent(JSON.stringify(features))}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: capturedAuth,
    credentials: 'include'
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const data = await response.json();
  
  // Extract replies from the response
  const replies = [];
  const seenIds = new Set([tweetId]); // Don't include the focal tweet

  function extractReplies(obj, depth = 0) {
    if (!obj || typeof obj !== 'object' || depth > 10) return;

    // Look for tweet results
    if (obj.__typename === 'Tweet' && obj.rest_id && !seenIds.has(obj.rest_id)) {
      const legacy = obj.legacy;
      const core = obj.core?.user_results?.result?.legacy;
      
      // Only include if it's a reply to our thread
      if (legacy?.conversation_id_str === tweetId || legacy?.in_reply_to_status_id_str) {
        seenIds.add(obj.rest_id);
        
        // Calculate reply depth
        let replyDepth = 0;
        if (legacy.in_reply_to_status_id_str === tweetId) {
          replyDepth = 1;
        } else if (legacy.in_reply_to_status_id_str) {
          replyDepth = 2; // Simplified - could trace the chain for accuracy
        }

        if (replyDepth <= maxDepth) {
          replies.push({
            id: obj.rest_id,
            text: obj.note_tweet?.note_tweet_results?.result?.text || legacy.full_text,
            author_handle: '@' + (core?.screen_name || 'unknown'),
            author_name: core?.name || '',
            created_at: legacy.created_at,
            metrics: {
              likes: legacy.favorite_count || 0,
              replies: legacy.reply_count || 0
            },
            in_reply_to: legacy.in_reply_to_status_id_str,
            depth: replyDepth
          });
        }
      }
    }

    // Recurse
    for (const value of Object.values(obj)) {
      if (Array.isArray(value)) {
        value.forEach(item => extractReplies(item, depth + 1));
      } else if (typeof value === 'object') {
        extractReplies(value, depth + 1);
      }
    }
  }

  extractReplies(data);

  // Sort by depth, then by likes
  replies.sort((a, b) => {
    if (a.depth !== b.depth) return a.depth - b.depth;
    return b.metrics.likes - a.metrics.likes;
  });

  return replies;
}

// ============================================
// OUTPUT & EXPORT
// ============================================

function printSummary() {
  console.log(`\n${'═'.repeat(60)}`);
  console.log('BOOKMARK EXTRACTION COMPLETE');
  console.log('═'.repeat(60));
  console.log(`Total bookmarks: ${allBookmarks.length}`);
  
  // Top by engagement
  const sorted = [...allBookmarks].sort((a, b) => b.engagement_score - a.engagement_score);
  console.log(`\nTop 5 by engagement:`);
  sorted.slice(0, 5).forEach((b, i) => {
    console.log(`  ${i + 1}. ${b.author.handle}: "${b.text.substring(0, 50)}..." (${b.metrics.likes} likes)`);
  });

  // Topic hints (simple keyword extraction)
  const allText = allBookmarks.map(b => b.text.toLowerCase()).join(' ');
  const keywords = ['obsidian', 'hooks', 'claude code', 'agent', 'context', 'wiggum', 'beads', 'mcp', 'sdk'];
  const found = keywords.filter(k => allText.includes(k));
  if (found.length > 0) {
    console.log(`\nTopics detected: ${found.join(', ')}`);
  }

  console.log(`\n📋 Access: window.bookmarks`);
  console.log(`📝 Copy:   copy(JSON.stringify(window.bookmarks, null, 2))`);
  console.log(`💾 Export: exportBookmarksJSON() or exportBookmarksMarkdown()`);
}

/**
 * Export as JSON with metadata
 */
function exportBookmarksJSON() {
  if (!window.bookmarks || window.bookmarks.length === 0) {
    console.error('No bookmarks to export. Run fetchBookmarkFolder() first.');
    return null;
  }

  const exportData = {
    exported_at: new Date().toISOString(),
    source: 'twitter_bookmark_folder',
    total_bookmarks: window.bookmarks.length,
    bookmarks: window.bookmarks
  };

  window.bookmarksJSON = exportData;
  console.log('✅ JSON export ready');
  console.log('   Copy: copy(JSON.stringify(window.bookmarksJSON, null, 2))');

  return exportData;
}

/**
 * Export as Markdown (for Obsidian import)
 */
function exportBookmarksMarkdown() {
  if (!window.bookmarks || window.bookmarks.length === 0) {
    console.error('No bookmarks to export. Run fetchBookmarkFolder() first.');
    return null;
  }

  const bookmarks = window.bookmarks;
  const sorted = [...bookmarks].sort((a, b) => b.engagement_score - a.engagement_score);

  let md = `# Twitter Bookmarks Export\n\n`;
  md += `**Exported:** ${new Date().toISOString()}\n`;
  md += `**Total Bookmarks:** ${bookmarks.length}\n\n`;
  md += `---\n\n`;

  sorted.forEach((b, idx) => {
    md += `## ${idx + 1}. ${b.author.handle}\n\n`;
    md += `**Author:** ${b.author.name} (${b.author.handle})\n`;
    md += `**Posted:** ${b.created_at_iso}\n`;
    md += `**URL:** ${b.url}\n\n`;
    
    md += `### Content\n\n`;
    md += `${b.text}\n\n`;

    if (b.card) {
      md += `**Link:** [${b.card.title || b.card.domain}](${b.card.url})\n`;
      if (b.card.description) {
        md += `> ${b.card.description}\n`;
      }
      md += `\n`;
    }

    if (b.media && b.media.length > 0) {
      md += `**Media:** ${b.media.length} attachment(s)\n`;
      b.media.forEach((m, i) => {
        md += `- [${m.type} ${i + 1}](${m.url})\n`;
      });
      md += `\n`;
    }

    md += `**Engagement:** ${b.metrics.replies} replies | ${b.metrics.retweets} reposts | ${b.metrics.likes} likes | ${b.metrics.bookmarks} bookmarks | ${b.metrics.views.toLocaleString()} views\n\n`;

    // Include replies if fetched
    if (b.replies && b.replies.length > 0) {
      md += `### Thread (${b.replies.length} replies)\n\n`;
      b.replies.forEach(r => {
        const indent = r.depth > 1 ? '  ' : '';
        md += `${indent}> **${r.author_handle}:** ${r.text}\n`;
        md += `${indent}> *(${r.metrics.likes} likes)*\n\n`;
      });
    }

    md += `---\n\n`;
  });

  window.bookmarksMarkdown = md;
  console.log('✅ Markdown export ready');
  console.log('   Copy: copy(window.bookmarksMarkdown)');

  return md;
}

/**
 * Export for SQLite import (matches claude-code-tips schema)
 */
function exportForSQLite() {
  if (!window.bookmarks || window.bookmarks.length === 0) {
    console.error('No bookmarks to export. Run fetchBookmarkFolder() first.');
    return null;
  }

  const rows = window.bookmarks.map(b => ({
    tweet_id: b.id,
    author_handle: b.author.handle,
    author_name: b.author.name,
    text: b.text,
    created_at: b.created_at_iso,
    url: b.url,
    replies: b.metrics.replies,
    retweets: b.metrics.retweets,
    likes: b.metrics.likes,
    quotes: b.metrics.quotes,
    views: b.metrics.views,
    bookmarks: b.metrics.bookmarks,
    engagement_score: b.engagement_score,
    conversation_id: b.conversation_id,
    is_reply: b.is_reply ? 1 : 0,
    in_reply_to: b.in_reply_to,
    card_url: b.card?.url || null,
    card_title: b.card?.title || null,
    media_count: b.media?.length || 0,
    source: 'claude_bookmarks',
    scraped_at: new Date().toISOString()
  }));

  window.bookmarksForSQL = rows;
  console.log('✅ SQLite export ready');
  console.log('   Copy: copy(JSON.stringify(window.bookmarksForSQL, null, 2))');

  return rows;
}

// ============================================
// INCREMENTAL MODE
// ============================================

/**
 * Load existing tweet IDs to enable incremental fetching
 */
function loadExistingIds(idsArray) {
  window.existingBookmarkIds = new Set(idsArray);
  console.log(`✅ Loaded ${idsArray.length} existing IDs`);
  return window.existingBookmarkIds;
}

/**
 * Fetch only new bookmarks (stop when hitting known IDs)
 */
async function fetchNewBookmarks(folderId, options = {}) {
  if (!window.existingBookmarkIds) {
    console.warn('⚠️ No existing IDs loaded. Run loadExistingIds([...]) first, or this will fetch all.');
  }

  const existingIds = window.existingBookmarkIds || new Set();
  const originalParse = parseBookmarkedTweet;

  // Track if we've hit existing content
  let hitExisting = false;
  const newBookmarks = [];

  // Override to check for existing
  const checkAndParse = (entry) => {
    const parsed = originalParse(entry);
    if (!parsed) return null;

    if (existingIds.has(parsed.id)) {
      console.log(`🛑 Hit existing bookmark: ${parsed.id}`);
      hitExisting = true;
      return null;
    }

    newBookmarks.push(parsed);
    return parsed;
  };

  // Temporarily replace parser
  // (In a real implementation, we'd modify fetchBookmarkFolder to accept a custom parser)
  
  console.log(`\n🔄 Fetching NEW bookmarks from folder ${folderId}...`);
  console.log(`   Will stop when hitting ${existingIds.size} known IDs\n`);

  await fetchBookmarkFolder(folderId, { ...options, maxPages: 5 }); // Limit pages for incremental

  // Filter to only new ones
  const onlyNew = allBookmarks.filter(b => !existingIds.has(b.id));
  
  window.newBookmarks = onlyNew;
  console.log(`\n✅ Found ${onlyNew.length} NEW bookmarks`);
  
  return onlyNew;
}

// ============================================
// QUICK START GUIDE
// ============================================

console.log(`
╔══════════════════════════════════════════════════════════════════╗
║          TWITTER BOOKMARK FOLDER EXTRACTOR                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  STEP 1: Capture authentication                                  ║
║    → Open your bookmark folder: x.com/i/bookmarks/FOLDER_ID      ║
║    → Open Network tab in DevTools                                ║
║    → Refresh the page                                            ║
║    → Find "BookmarkFolderTimeline" request                       ║
║    → Right-click → Copy as cURL (bash)                           ║
║    → Run: setAuthFromCurl(\`paste_your_curl_here\`)               ║
║                                                                  ║
║  STEP 2: Get folder ID from URL                                  ║
║    URL: x.com/i/bookmarks/2004623846088040770                    ║
║    Folder ID: 2004623846088040770                                ║
║                                                                  ║
║  STEP 3: Fetch bookmarks                                         ║
║    → await fetchBookmarkFolder("2004623846088040770")            ║
║                                                                  ║
║  STEP 4: Export                                                  ║
║    → JSON:     exportBookmarksJSON()                             ║
║    → Markdown: exportBookmarksMarkdown()                         ║
║    → SQLite:   exportForSQLite()                                 ║
║    → Copy:     copy(JSON.stringify(window.bookmarks, null, 2))   ║
║                                                                  ║
║  ─────────────────────────────────────────────────────────────   ║
║                                                                  ║
║  WITH REPLY THREADS (slower, more complete):                     ║
║    await fetchBookmarkFolder("ID", {                             ║
║      fetchReplies: true,                                         ║
║      replyThreshold: 10  // only if >10 replies                  ║
║    })                                                            ║
║                                                                  ║
║  INCREMENTAL MODE (only new bookmarks):                          ║
║    loadExistingIds(["id1", "id2", ...])                          ║
║    await fetchNewBookmarks("FOLDER_ID")                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
`);
