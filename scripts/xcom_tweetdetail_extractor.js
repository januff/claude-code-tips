/**
 * TweetDetail GraphQL extractor for x.com content.
 *
 * Inject this into an x.com tab via Claude-in-Chrome javascript_tool.
 * Requires an authenticated x.com session (ct0 cookie + auth_token httpOnly cookie).
 *
 * Usage:
 *   1. Inject this script into an x.com tab
 *   2. Call: const results = await window._extractXcomContent(urls)
 *      where urls = [{ link_id, url, tweet_id? }, ...]
 *   3. Write results to DOM: document.body.innerText = JSON.stringify(results)
 *   4. Read via get_page_text tool (bypasses javascript_tool 1500 char limit)
 *
 * Hash update: If TweetDetail returns errors, capture a fresh hash from
 * network requests on any tweet page (filter for "TweetDetail" in URL).
 */

// TweetDetail hash — update when Twitter rotates it
const TWEET_DETAIL_HASH = '7U1X7-LeNUX-OYmIndrSiw';

window._fetchTweetDetail = async function(tweetId) {
  const variables = {
    focalTweetId: tweetId,
    with_rux_injections: false,
    rankingMode: "Relevance",
    includePromotedContent: true,
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

  // Critical: withArticleRichContentState enables article content in response
  const fieldToggles = {
    withArticleRichContentState: true,
    withArticlePlainText: false,
    withGrokAnalyze: false,
    withDisallowedReplyControls: false
  };

  const params = new URLSearchParams({
    variables: JSON.stringify(variables),
    features: JSON.stringify(features),
    fieldToggles: JSON.stringify(fieldToggles)
  });

  const url = `https://x.com/i/api/graphql/${TWEET_DETAIL_HASH}/TweetDetail?${params}`;
  const ct0 = document.cookie.split('; ').find(c => c.startsWith('ct0='))?.split('=')[1];

  const resp = await fetch(url, {
    headers: {
      'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
      'x-csrf-token': ct0,
      'content-type': 'application/json',
      'x-twitter-active-user': 'yes',
      'x-twitter-auth-type': 'OAuth2Session'
    },
    credentials: 'include'
  });

  if (!resp.ok) throw new Error(`TweetDetail failed: ${resp.status}`);
  return await resp.json();
};

window._extractXcomContent = async function(urls) {
  const results = [];

  for (const urlObj of urls) {
    const { link_id, url, tweet_id: dbTweetId } = urlObj;

    // Extract tweet ID from URL
    let tweetId = null;
    const statusMatch = url.match(/\/status\/(\d+)/);
    const articleMatch = url.match(/\/article\/(\d+)/);

    if (statusMatch) {
      tweetId = statusMatch[1];
    } else if (articleMatch) {
      tweetId = dbTweetId || articleMatch[1];
    }

    if (!tweetId) {
      results.push({ link_id, url, error: 'Could not extract tweet ID' });
      continue;
    }

    try {
      const data = await window._fetchTweetDetail(tweetId);
      const entries = data?.data?.threaded_conversation_with_injections_v2?.instructions
        ?.find(i => i.type === 'TimelineAddEntries')?.entries || [];

      const focal = entries.find(e => e.entryId?.includes(tweetId));
      if (!focal) {
        results.push({ link_id, url, tweetId, error: 'Tweet not found in response' });
        continue;
      }

      const tweetResult = focal.content?.itemContent?.tweet_results?.result;
      const legacy = tweetResult?.legacy || tweetResult?.tweet?.legacy;
      const user = tweetResult?.core?.user_results?.result?.legacy ||
                   tweetResult?.tweet?.core?.user_results?.result?.legacy;

      let content = '';
      let contentType = 'tweet';
      let title = '';

      // 1. Article content (Draft.js blocks)
      const article = tweetResult?.article?.article_results?.result;
      if (article?.content_state?.blocks) {
        content = article.content_state.blocks.map(b => b.text).filter(t => t).join('\n');
        contentType = 'article';
        title = article.content_state.blocks[0]?.text || '';
      }

      // 2. Note tweet (long-form)
      const noteText = tweetResult?.note_tweet?.note_tweet_results?.result?.text;
      if (noteText && (!content || content.length < noteText.length)) {
        content = noteText;
        contentType = 'note_tweet';
      }

      // 3. Regular tweet text
      if (!content) {
        content = legacy?.full_text || '';
        contentType = 'tweet';
      }

      results.push({
        link_id, url, tweetId,
        author: user?.screen_name || '',
        contentType, title, content,
        contentLength: content.length,
        likes: legacy?.favorite_count || 0
      });

      await new Promise(r => setTimeout(r, 500));
    } catch (e) {
      results.push({ link_id, url, tweetId, error: e.message });
    }
  }

  return results;
};
