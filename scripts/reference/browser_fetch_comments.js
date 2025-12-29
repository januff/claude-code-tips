/**
 * Sora Comments Fetcher - Browser Console Script
 * 
 * Run this in your browser console while logged into sora.chatgpt.com
 * 
 * Usage:
 *   1. Open sora.chatgpt.com and ensure you're logged in
 *   2. Open Developer Tools (Cmd+Option+I)
 *   3. Go to Console tab
 *   4. Paste this entire script and press Enter
 *   5. Call: await fetchCommentsForVideos(videoIds)
 *   6. Results will be in window.soraComments
 */

// Configuration
const COMMENTS_API_BASE = 'https://sora.chatgpt.com/backend/project_y/post';
const DEFAULT_LIMIT = 50;  // Max comments per request
const DEFAULT_MAX_DEPTH = 2;  // Include nested replies
const REQUEST_DELAY = 300;  // ms between requests to avoid rate limiting

/**
 * Sleep utility
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Parse a single comment item from the API response
 */
function parseComment(item, parentId = null) {
  const post = item.post;
  const profile = item.profile;
  
  const comment = {
    comment_id: post.id,
    text: post.text,
    author_username: profile?.username || null,
    author_display_name: profile?.display_name || null,
    author_id: post.shared_by,
    like_count: post.like_count || 0,
    reply_count: post.reply_count || 0,
    posted_at: post.posted_at,  // Unix timestamp
    posted_at_iso: post.posted_at ? new Date(post.posted_at * 1000).toISOString() : null,
    parent_comment_id: parentId,
    profile_picture_url: profile?.profile_picture_url || null,
    permalink: post.permalink
  };
  
  // Parse nested replies if present
  const nestedReplies = [];
  if (item.children?.items?.length > 0) {
    for (const child of item.children.items) {
      const childComment = parseComment(child, post.id);
      nestedReplies.push(childComment);
      // Recursively get deeply nested replies
      if (child.children?.items?.length > 0) {
        for (const grandchild of child.children.items) {
          nestedReplies.push(parseComment(grandchild, child.post.id));
        }
      }
    }
  }
  
  return { comment, replies: nestedReplies };
}

/**
 * Fetch comments for a single video
 */
async function fetchCommentsForVideo(postId, options = {}) {
  const limit = options.limit || DEFAULT_LIMIT;
  const maxDepth = options.maxDepth || DEFAULT_MAX_DEPTH;
  
  // Ensure post ID has the s_ prefix if it's a video post
  const fullPostId = postId.startsWith('s_') ? postId : `s_${postId}`;
  
  const url = `${COMMENTS_API_BASE}/${fullPostId}/tree?limit=${limit}&max_depth=${maxDepth}`;
  
  try {
    const response = await fetch(url, {
      method: 'GET',
      credentials: 'include',  // Include cookies for auth
      headers: {
        'Accept': 'application/json',
      }
    });
    
    if (!response.ok) {
      console.error(`Failed to fetch comments for ${postId}: HTTP ${response.status}`);
      return { post_id: postId, comments: [], error: `HTTP ${response.status}` };
    }
    
    const data = await response.json();
    
    // Extract post metadata
    const postMeta = {
      post_id: data.post?.id,
      title: data.post?.text,
      creator_username: data.profile?.username,
      like_count: data.post?.like_count,
      view_count: data.post?.view_count,
      remix_count: data.post?.remix_count,
      reply_count: data.post?.reply_count,
      recursive_reply_count: data.post?.recursive_reply_count
    };
    
    // Parse comments from children
    const comments = [];
    if (data.children?.items?.length > 0) {
      for (const item of data.children.items) {
        const { comment, replies } = parseComment(item);
        comments.push(comment);
        comments.push(...replies);  // Flatten nested replies
      }
    }
    
    // Check for pagination cursor
    const cursor = data.children?.cursor || null;
    
    return {
      post_id: postId,
      post_metadata: postMeta,
      comments: comments,
      total_comments: comments.length,
      has_more: cursor !== null,
      cursor: cursor
    };
    
  } catch (error) {
    console.error(`Error fetching comments for ${postId}:`, error);
    return { post_id: postId, comments: [], error: error.message };
  }
}

/**
 * Fetch comments for multiple videos
 */
async function fetchCommentsForVideos(postIds, options = {}) {
  const results = [];
  const delay = options.delay || REQUEST_DELAY;
  
  console.log(`Fetching comments for ${postIds.length} videos...`);
  
  for (let i = 0; i < postIds.length; i++) {
    const postId = postIds[i];
    console.log(`[${i + 1}/${postIds.length}] Fetching: ${postId}`);
    
    const result = await fetchCommentsForVideo(postId, options);
    results.push(result);
    
    console.log(`  → ${result.total_comments || 0} comments`);
    
    // Delay between requests
    if (i < postIds.length - 1) {
      await sleep(delay);
    }
  }
  
  // Store in global for easy access
  window.soraComments = results;
  
  // Summary
  const totalComments = results.reduce((sum, r) => sum + (r.total_comments || 0), 0);
  const errors = results.filter(r => r.error).length;
  
  console.log('\n=== SUMMARY ===');
  console.log(`Videos processed: ${results.length}`);
  console.log(`Total comments: ${totalComments}`);
  console.log(`Errors: ${errors}`);
  console.log('\nResults stored in window.soraComments');
  console.log('To copy: copy(JSON.stringify(window.soraComments, null, 2))');
  
  return results;
}

/**
 * Fetch comments for all videos from your likes data
 * Requires window.soraLikes or a loaded sora_likes_enhanced.json
 */
async function fetchCommentsForAllLikes(likesData = null) {
  // Try to get likes data from various sources
  let videos = likesData || window.soraLikes || window.allLikes;
  
  if (!videos || !Array.isArray(videos)) {
    console.error('No likes data found. Please provide likesData or set window.soraLikes');
    console.log('Example: await fetchCommentsForAllLikes(JSON.parse(yourLikesJson))');
    return null;
  }
  
  // Extract post IDs
  const postIds = videos.map(v => v.fullId || v.full_id || `s_${v.videoId || v.video_id}`);
  
  console.log(`Found ${postIds.length} videos to fetch comments for`);
  
  return await fetchCommentsForVideos(postIds);
}

/**
 * Export comments to a format ready for merging with analysis data
 */
function exportCommentsForMerge() {
  if (!window.soraComments) {
    console.error('No comments data. Run fetchCommentsForVideos first.');
    return null;
  }
  
  const exportData = {
    fetched_at: new Date().toISOString(),
    total_videos: window.soraComments.length,
    total_comments: window.soraComments.reduce((sum, r) => sum + (r.total_comments || 0), 0),
    videos: {}
  };
  
  for (const result of window.soraComments) {
    // Extract just the video ID (without s_ prefix)
    const videoId = result.post_id.replace(/^s_/, '');
    
    exportData.videos[videoId] = {
      comment_count: result.total_comments,
      comments: result.comments.map(c => ({
        id: c.comment_id,
        text: c.text,
        author: c.author_username,
        author_display_name: c.author_display_name,
        author_id: c.author_id,
        likes: c.like_count,
        posted_at: c.posted_at_iso,
        parent_id: c.parent_comment_id
      }))
    };
  }
  
  window.commentsExport = exportData;
  console.log('Export ready in window.commentsExport');
  console.log('To copy: copy(JSON.stringify(window.commentsExport, null, 2))');
  
  return exportData;
}

/**
 * Load video IDs from a local JSON file (like sora_likes_enhanced.json)
 * Opens a file picker dialog
 */
async function loadVideoIdsFromFile() {
  return new Promise((resolve, reject) => {
    // Create hidden file input
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    
    input.onchange = async (event) => {
      const file = event.target.files[0];
      if (!file) {
        reject(new Error('No file selected'));
        return;
      }
      
      try {
        const text = await file.text();
        const data = JSON.parse(text);
        
        // Handle different JSON structures
        let videos = Array.isArray(data) ? data : data.videos || data.items || data.results || [];
        
        // Extract video IDs
        const videoIds = videos.map(v => {
          const id = v.fullId || v.full_id || v.videoId || v.video_id || v.id;
          // Ensure s_ prefix for video posts
          if (id && !id.startsWith('s_') && id.length === 32) {
            return `s_${id}`;
          }
          return id;
        }).filter(Boolean);
        
        console.log(`Loaded ${videoIds.length} video IDs from ${file.name}`);
        
        // Store for easy access
        window.loadedVideoIds = videoIds;
        
        resolve(videoIds);
      } catch (error) {
        reject(new Error(`Failed to parse JSON: ${error.message}`));
      }
    };
    
    input.oncancel = () => reject(new Error('File selection cancelled'));
    
    // Trigger file picker
    input.click();
  });
}

/**
 * Load previous comments export to find videos needing retry
 */
async function loadPreviousCommentsExport() {
  return new Promise((resolve, reject) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    
    input.onchange = async (event) => {
      const file = event.target.files[0];
      if (!file) {
        reject(new Error('No file selected'));
        return;
      }
      
      try {
        const text = await file.text();
        const data = JSON.parse(text);
        
        // Find videos with 0 comments (potential failures)
        const zeroCommentIds = [];
        const hasCommentsIds = [];
        
        const videos = data.videos || {};
        for (const [videoId, videoData] of Object.entries(videos)) {
          if (videoData.comment_count === 0) {
            zeroCommentIds.push(`s_${videoId}`);
          } else {
            hasCommentsIds.push(`s_${videoId}`);
          }
        }
        
        console.log(`Found ${zeroCommentIds.length} videos with 0 comments to retry`);
        console.log(`Skipping ${hasCommentsIds.length} videos that already have comments`);
        
        window.retryVideoIds = zeroCommentIds;
        window.alreadyHaveComments = hasCommentsIds;
        
        resolve(zeroCommentIds);
      } catch (error) {
        reject(new Error(`Failed to parse JSON: ${error.message}`));
      }
    };
    
    input.oncancel = () => reject(new Error('File selection cancelled'));
    input.click();
  });
}

/**
 * Fetch comments with batching and pauses to avoid rate limiting
 */
async function fetchCommentsWithBatching(videoIds, options = {}) {
  const batchSize = options.batchSize || 100;
  const delayBetweenRequests = options.delay || 1500;  // 1.5s between requests
  const pauseBetweenBatches = options.pauseBetweenBatches || 60000;  // 60s between batches
  
  const allResults = [];
  const totalBatches = Math.ceil(videoIds.length / batchSize);
  
  console.log(`\n📦 Processing ${videoIds.length} videos in ${totalBatches} batches`);
  console.log(`   Delay between requests: ${delayBetweenRequests}ms`);
  console.log(`   Pause between batches: ${pauseBetweenBatches/1000}s\n`);
  
  for (let batchNum = 0; batchNum < totalBatches; batchNum++) {
    const start = batchNum * batchSize;
    const end = Math.min(start + batchSize, videoIds.length);
    const batch = videoIds.slice(start, end);
    
    console.log(`\n═══════════════════════════════════════`);
    console.log(`BATCH ${batchNum + 1}/${totalBatches} (videos ${start + 1}-${end})`);
    console.log(`═══════════════════════════════════════\n`);
    
    // Process batch
    for (let i = 0; i < batch.length; i++) {
      const videoId = batch[i];
      const globalIdx = start + i + 1;
      console.log(`[${globalIdx}/${videoIds.length}] Fetching: ${videoId}`);
      
      const result = await fetchCommentsForVideo(videoId, options);
      allResults.push(result);
      
      if (result.error) {
        console.log(`  ❌ Error: ${result.error}`);
      } else {
        console.log(`  → ${result.total_comments || 0} comments`);
      }
      
      // Delay between requests within batch
      if (i < batch.length - 1) {
        await sleep(delayBetweenRequests);
      }
    }
    
    // Save checkpoint after each batch
    window.soraCommentsCheckpoint = allResults.slice();
    console.log(`\n💾 Checkpoint saved: ${allResults.length} videos processed`);
    
    // Pause between batches (except after last batch)
    if (batchNum < totalBatches - 1) {
      console.log(`\n⏸️  Pausing ${pauseBetweenBatches/1000}s before next batch to avoid rate limits...`);
      console.log(`   (Checkpoint available in window.soraCommentsCheckpoint)`);
      await sleep(pauseBetweenBatches);
    }
  }
  
  window.soraComments = allResults;
  
  // Summary
  const totalComments = allResults.reduce((sum, r) => sum + (r.total_comments || 0), 0);
  const errors = allResults.filter(r => r.error).length;
  
  console.log('\n═══════════════════════════════════════');
  console.log('FINAL SUMMARY');
  console.log('═══════════════════════════════════════');
  console.log(`Videos processed: ${allResults.length}`);
  console.log(`Total comments: ${totalComments}`);
  console.log(`Errors: ${errors}`);
  console.log('\nResults in window.soraComments');
  
  return allResults;
}

/**
 * Retry only videos that had 0 comments (potential failures)
 * Load your previous comments_all.json to identify these
 */
async function retryZeroCommentVideos(options = {}) {
  console.log('Select your previous comments export (comments_all.json)...');
  
  try {
    const videoIds = await loadPreviousCommentsExport();
    
    if (videoIds.length === 0) {
      console.log('✅ No videos need retry - all have comments!');
      return null;
    }
    
    const estimatedMinutes = Math.ceil(
      (videoIds.length * (options.delay || 1500) + 
       Math.floor(videoIds.length / 100) * (options.pauseBetweenBatches || 60000)) / 60000
    );
    
    console.log(`\n⏱️  Estimated time: ${estimatedMinutes} minutes`);
    console.log(`   (${videoIds.length} videos × 1.5s delay + batch pauses)\n`);
    
    const results = await fetchCommentsWithBatching(videoIds, {
      delay: 1500,
      batchSize: 100,
      pauseBetweenBatches: 60000,
      ...options
    });
    
    // Export retry results
    window.retryResults = results;
    exportRetryResults();
    
    return results;
  } catch (error) {
    console.error('Error:', error.message);
    return null;
  }
}

/**
 * Export retry results in format ready to merge
 */
function exportRetryResults() {
  if (!window.soraComments) {
    console.error('No retry results. Run retryZeroCommentVideos first.');
    return null;
  }
  
  const exportData = {
    fetched_at: new Date().toISOString(),
    is_retry: true,
    total_videos: window.soraComments.length,
    total_comments: window.soraComments.reduce((sum, r) => sum + (r.total_comments || 0), 0),
    errors: window.soraComments.filter(r => r.error).length,
    videos: {}
  };
  
  for (const result of window.soraComments) {
    const videoId = result.post_id.replace(/^s_/, '');
    
    exportData.videos[videoId] = {
      comment_count: result.total_comments || 0,
      had_error: !!result.error,
      error: result.error || null,
      comments: (result.comments || []).map(c => ({
        id: c.comment_id,
        text: c.text,
        author: c.author_username,
        author_display_name: c.author_display_name,
        author_id: c.author_id,
        likes: c.like_count,
        posted_at: c.posted_at_iso,
        parent_id: c.parent_comment_id
      }))
    };
  }
  
  window.commentsRetryExport = exportData;
  console.log('\n📦 Retry export ready in window.commentsRetryExport');
  console.log('   To copy: copy(JSON.stringify(window.commentsRetryExport, null, 2))');
  
  return exportData;
}

/**
 * One-click: Load JSON file and fetch all comments
 */
async function fetchAllCommentsFromFile(options = {}) {
  console.log('Select your sora_likes_enhanced.json file...');
  
  try {
    const videoIds = await loadVideoIdsFromFile();
    
    console.log(`\nReady to fetch comments for ${videoIds.length} videos`);
    console.log(`Estimated time: ${Math.ceil(videoIds.length * (options.delay || 400) / 60000)} minutes\n`);
    
    // Fetch all comments
    const results = await fetchCommentsForVideos(videoIds, {
      delay: options.delay || 400,
      ...options
    });
    
    // Auto-export
    exportCommentsForMerge();
    
    console.log('\n✅ Complete! Run: copy(JSON.stringify(window.commentsExport, null, 2))');
    
    return results;
  } catch (error) {
    console.error('Error:', error.message);
    return null;
  }
}

// ========================================
// Quick Start Guide
// ========================================
console.log(`
╔══════════════════════════════════════════════════════════════════╗
║                 SORA COMMENTS FETCHER LOADED                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  🔄 RETRY MODE (recommended for fixing rate-limit failures):      ║
║     await retryZeroCommentVideos()                                ║
║     → Select your comments_all.json                               ║
║     → Retries only 0-comment videos with safe delays              ║
║     → ~20 min for 1000 videos (1.5s delay + batch pauses)         ║
║                                                                   ║
║  ─────────────────────────────────────────────────────────────    ║
║                                                                   ║
║  🆕 FRESH START - Fetch all from scratch:                         ║
║     await fetchAllCommentsFromFile()                              ║
║     → Select sora_likes_enhanced.json                             ║
║                                                                   ║
║  ─────────────────────────────────────────────────────────────    ║
║                                                                   ║
║  📋 RESULTS - After fetching:                                     ║
║     copy(JSON.stringify(window.commentsRetryExport, null, 2))     ║
║     or: copy(JSON.stringify(window.commentsExport, null, 2))      ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
`);
