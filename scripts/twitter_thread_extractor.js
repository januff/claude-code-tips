/**
 * Twitter/X Thread Extractor - API-based
 *
 * Extracts all replies from a Twitter thread via API (not DOM scraping).
 * Handles pagination, rate limiting, and outputs structured JSON.
 *
 * SETUP:
 * 1. Open the thread in your browser
 * 2. Open DevTools → Network tab
 * 3. Scroll to load some replies
 * 4. Find a request to "TweetDetail" in the Network tab
 * 5. Right-click → Copy as cURL
 * 6. Run: setAuthFromCurl(`paste_here`)
 * 7. Run: await fetchThreadReplies("TWEET_ID")
 *
 * Created: 2025-12-28
 */

// Storage
let capturedAuth = null;
let allTweets = [];

/**
 * Extract auth from cURL command
 * Handles format: -H 'header-name: value'
 */
function setAuthFromCurl(curlCommand) {
  // Extract headers from -H 'name: value' format
  const headerRegex = /-H\s+['"]([^:]+):\s*([^'"]+)['"]/gi;
  const headers = {};

  let match;
  while ((match = headerRegex.exec(curlCommand)) !== null) {
    const name = match[1].toLowerCase().trim();
    const value = match[2].trim();
    headers[name] = value;
  }

  // Also try to extract cookie if present
  const cookieMatch = curlCommand.match(/-H\s+['"]cookie:\s*([^'"]+)['"]/i);
  if (cookieMatch) {
    headers['cookie'] = cookieMatch[1];
  }

  // Check for required headers
  const csrfToken = headers['x-csrf-token'];

  if (!csrfToken) {
    console.error('❌ Could not find x-csrf-token in cURL command.');
    console.log('Found headers:', Object.keys(headers));
    return false;
  }

  // Twitter uses a static Bearer token for the GraphQL API
  // The real auth is in the cookie and csrf token
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

/**
 * Manually set auth if cURL parsing fails
 */
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

/**
 * Parse tweet data from API response
 */
function parseTweet(tweetResult) {
  try {
    const tweet = tweetResult?.tweet || tweetResult;
    const legacy = tweet?.legacy;
    const core = tweet?.core?.user_results?.result?.legacy;

    if (!legacy) return null;

    // Handle extended tweets (note_tweet) for long-form content
    // Priority: note_tweet > legacy.full_text > legacy.text
    const noteTweet = tweet?.note_tweet?.note_tweet_results?.result?.text;
    const tweetText = noteTweet || legacy.full_text || legacy.text || '';

    return {
      id: tweet.rest_id,
      text: tweetText,
      author_handle: '@' + (core?.screen_name || 'unknown'),
      author_name: core?.name || '',
      created_at: legacy.created_at,
      created_at_iso: new Date(legacy.created_at).toISOString(),
      url: `https://x.com/${core?.screen_name}/status/${tweet.rest_id}`,
      metrics: {
        replies: legacy.reply_count || 0,
        retweets: legacy.retweet_count || 0,
        likes: legacy.favorite_count || 0,
        quotes: legacy.quote_count || 0,
        views: parseInt(tweet.views?.count) || 0,
        bookmarks: legacy.bookmark_count || 0
      },
      media: (legacy.entities?.media || legacy.extended_entities?.media || []).map(m => ({
        type: m.type,
        url: m.media_url_https,
        expanded_url: m.expanded_url,
        alt_text: m.ext_alt_text || null
      })),
      is_reply_to: legacy.in_reply_to_status_id_str || null,
      conversation_id: legacy.conversation_id_str || null
    };
  } catch (e) {
    console.error('Parse error:', e);
    return null;
  }
}

/**
 * Extract tweets from nested API response
 */
function extractTweetsFromResponse(data) {
  const tweets = [];
  const seenIds = new Set();

  function recurse(obj, depth = 0) {
    if (!obj || typeof obj !== 'object' || depth > 20) return;

    // Check for tweet result
    if (obj.__typename === 'Tweet' && obj.rest_id) {
      const parsed = parseTweet(obj);
      if (parsed && !seenIds.has(parsed.id)) {
        seenIds.add(parsed.id);
        tweets.push(parsed);
      }
    }

    // Also check tweet_results wrapper
    if (obj.tweet_results?.result) {
      const parsed = parseTweet(obj.tweet_results.result);
      if (parsed && !seenIds.has(parsed.id)) {
        seenIds.add(parsed.id);
        tweets.push(parsed);
      }
    }

    // Recurse into children
    for (const value of Object.values(obj)) {
      if (Array.isArray(value)) {
        value.forEach(item => recurse(item, depth + 1));
      } else if (typeof value === 'object') {
        recurse(value, depth + 1);
      }
    }
  }

  recurse(data);
  return tweets;
}

/**
 * Find cursor for pagination
 */
function findCursor(data, cursorType = 'Bottom') {
  let cursor = null;

  function recurse(obj) {
    if (!obj || typeof obj !== 'object' || cursor) return;

    // Check for cursor entries
    if (obj.entryId && obj.entryId.includes(`cursor-bottom`)) {
      cursor = obj.content?.itemContent?.value || obj.content?.value;
      return;
    }

    // Check cursorType in content
    if (obj.cursorType === cursorType || obj.cursorType === 'Bottom') {
      cursor = obj.value;
      return;
    }

    for (const value of Object.values(obj)) {
      if (Array.isArray(value)) {
        value.forEach(recurse);
      } else if (typeof value === 'object') {
        recurse(value);
      }
    }
  }

  recurse(data);
  return cursor;
}

/**
 * Fetch thread replies using Twitter's GraphQL API
 */
async function fetchThreadReplies(tweetId, options = {}) {
  const maxPages = options.maxPages || 100;
  const delay = options.delay || 2000;

  if (!capturedAuth) {
    console.error('❌ No auth. Run setAuthFromCurl(`your_curl_command`) first.');
    console.log('\nTo get cURL:');
    console.log('1. Open Network tab in DevTools');
    console.log('2. Scroll to load replies');
    console.log('3. Find "TweetDetail" request');
    console.log('4. Right-click → Copy as cURL');
    return [];
  }

  // Reset storage
  allTweets = [];
  const seenIds = new Set();

  // Twitter's TweetDetail GraphQL endpoint (extract from your cURL if different)
  const baseUrl = 'https://x.com/i/api/graphql/nBS-WpgA6ZG0CyNHD517JQ/TweetDetail';

  // GraphQL variables
  const baseVariables = {
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

  let cursor = null;
  let pageNum = 0;
  let consecutiveEmpty = 0;

  console.log(`\n🔍 Fetching replies for tweet ${tweetId}...`);
  console.log(`   Delay between requests: ${delay}ms\n`);

  while (pageNum < maxPages && consecutiveEmpty < 3) {
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
      const tweets = extractTweetsFromResponse(data);

      let newCount = 0;
      for (const tweet of tweets) {
        if (!seenIds.has(tweet.id)) {
          seenIds.add(tweet.id);
          allTweets.push(tweet);
          newCount++;
        }
      }

      console.log(`   → ${newCount} new tweets (Total: ${allTweets.length})`);

      if (newCount === 0) {
        consecutiveEmpty++;
      } else {
        consecutiveEmpty = 0;
      }

      // Find next cursor
      const nextCursor = findCursor(data);

      if (!nextCursor || nextCursor === cursor) {
        console.log('📄 No more pages');
        break;
      }

      cursor = nextCursor;

      // Checkpoint save
      window.twitterThreadCheckpoint = allTweets.slice();

      // Rate limit delay
      await new Promise(r => setTimeout(r, delay));

    } catch (e) {
      console.error('Error:', e.message);
      break;
    }
  }

  // Store final results
  window.twitterThread = allTweets;

  // Summary
  console.log(`\n${'═'.repeat(50)}`);
  console.log('COMPLETE');
  console.log('═'.repeat(50));
  console.log(`Total tweets: ${allTweets.length}`);
  console.log(`Pages fetched: ${pageNum}`);
  console.log('');
  console.log('📋 Access: window.twitterThread');
  console.log('📝 Copy:   copy(JSON.stringify(window.twitterThread, null, 2))');
  console.log('💾 Export: exportToMarkdown()');

  return allTweets;
}

/**
 * Export to markdown format matching the project's tip format
 */
function exportToMarkdown() {
  if (!window.twitterThread || window.twitterThread.length === 0) {
    console.error('No tweets to export. Run fetchThreadReplies() first.');
    return null;
  }

  const tweets = window.twitterThread;

  // Sort by engagement (likes)
  const sorted = [...tweets].sort((a, b) =>
    (b.metrics.likes || 0) - (a.metrics.likes || 0)
  );

  let md = `# Twitter Thread Export\n\n`;
  md += `**Exported:** ${new Date().toISOString()}\n`;
  md += `**Total Tweets:** ${tweets.length}\n\n`;
  md += `---\n\n`;

  sorted.forEach((tweet, idx) => {
    md += `### ${idx + 1}. ${tweet.author_handle}\n`;
    md += `**Author:** ${tweet.author_handle} (${tweet.author_name})\n`;
    md += `**Posted:** ${tweet.created_at_iso}\n`;
    md += `**Tip:** ${tweet.text}\n`;

    if (tweet.media && tweet.media.length > 0) {
      md += `**Images:** ${tweet.media.length} image(s)\n`;
      tweet.media.forEach((m, i) => {
        md += `  - [Image ${i + 1}](${m.url})${m.alt_text ? ` - ${m.alt_text}` : ''}\n`;
      });
    } else {
      md += `**Images:** None\n`;
    }

    md += `**Engagement:** ${tweet.metrics.replies} replies | ${tweet.metrics.retweets} reposts | ${tweet.metrics.likes} likes | ${tweet.metrics.bookmarks} bookmarks | ${tweet.metrics.views.toLocaleString()} views\n`;
    md += `**URL:** ${tweet.url}\n`;
    md += `\n---\n\n`;
  });

  window.twitterThreadMarkdown = md;
  console.log('✅ Markdown export ready in window.twitterThreadMarkdown');
  console.log('   Copy: copy(window.twitterThreadMarkdown)');

  return md;
}

/**
 * Export as JSON with metadata
 */
function exportToJSON() {
  if (!window.twitterThread || window.twitterThread.length === 0) {
    console.error('No tweets to export. Run fetchThreadReplies() first.');
    return null;
  }

  const exportData = {
    exported_at: new Date().toISOString(),
    total_tweets: window.twitterThread.length,
    tweets: window.twitterThread
  };

  window.twitterThreadJSON = exportData;
  console.log('✅ JSON export ready');
  console.log('   Copy: copy(JSON.stringify(window.twitterThreadJSON, null, 2))');

  return exportData;
}

// ========================================
// Quick Start Guide
// ========================================
console.log(`
╔══════════════════════════════════════════════════════════════════╗
║            TWITTER/X THREAD EXTRACTOR (API-based)                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  STEP 1: Capture authentication                                   ║
║    → Open Network tab in DevTools                                 ║
║    → Scroll the thread to load some replies                       ║
║    → Find request containing "TweetDetail"                        ║
║    → Right-click → Copy as cURL (bash)                            ║
║    → Run: setAuthFromCurl(\`paste_your_curl_here\`)               ║
║                                                                   ║
║  STEP 2: Get the tweet ID from URL                                ║
║    Example URL: x.com/alexalbert__/status/1873754311106740359     ║
║    Tweet ID: 1873754311106740359                                  ║
║                                                                   ║
║  STEP 3: Fetch all replies                                        ║
║    → await fetchThreadReplies("1873754311106740359")              ║
║                                                                   ║
║  STEP 4: Export                                                   ║
║    → JSON: copy(JSON.stringify(window.twitterThread, null, 2))    ║
║    → Markdown: exportToMarkdown(); copy(window.twitterThreadMarkdown) ║
║                                                                   ║
║  ─────────────────────────────────────────────────────────────    ║
║                                                                   ║
║  MANUAL AUTH (if cURL parsing fails):                             ║
║    1. In Network tab, find TweetDetail request                    ║
║    2. Look at Request Headers                                     ║
║    3. Copy x-csrf-token value                                     ║
║    4. Run: setAuthManual("your-csrf-token-here")                  ║
║                                                                   ║
║  TROUBLESHOOTING:                                                 ║
║    - 401/403 error: Auth expired, re-capture cURL                 ║
║    - 429 error: Rate limited, script will auto-wait               ║
║    - Empty results: Try different tweet ID or re-auth             ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
`);
