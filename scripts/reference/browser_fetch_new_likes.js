/**
 * Fetch New Likes - Incremental version
 * 
 * Stops when it hits video IDs that are already in your collection.
 * 
 * SETUP:
 * 1. Load existing IDs: await loadExistingIdsFromFile()
 * 2. Capture auth: await captureAuth() (triggers a request to grab headers)
 * 3. Fetch: await fetchNewLikes()
 */

// Store captured auth headers
let capturedAuth = null;

/**
 * Capture auth headers by making a test request
 * You may need to reload the page if this fails
 */
async function captureAuth() {
  // Try to get auth from the page's existing state
  // Method 1: Check if there's an Authorization in localStorage/sessionStorage
  const possibleTokens = [
    sessionStorage.getItem('oai-token'),
    localStorage.getItem('oai-token'),
  ].filter(Boolean);
  
  if (possibleTokens.length > 0) {
    capturedAuth = { authorization: `Bearer ${possibleTokens[0]}` };
    console.log('✅ Found auth token in storage');
    return capturedAuth;
  }
  
  // Method 2: User provides from Network tab
  console.log('');
  console.log('🔐 AUTH REQUIRED');
  console.log('================');
  console.log('1. Open Network tab in DevTools');
  console.log('2. Refresh the page or click around to trigger a request');
  console.log('3. Find a request to sora.chatgpt.com/backend/...');
  console.log('4. Right-click → Copy → Copy as cURL');
  console.log('5. Run: setAuthFromCurl(`paste_curl_here`)');
  console.log('');
  console.log('OR manually set:');
  console.log('  setAuth("Bearer YOUR_TOKEN_HERE")');
  
  return null;
}

function setAuth(bearerToken) {
  const token = bearerToken.startsWith('Bearer ') ? bearerToken : `Bearer ${bearerToken}`;
  capturedAuth = { authorization: token };
  console.log('✅ Auth set successfully');
  return capturedAuth;
}

function setAuthFromCurl(curlCommand) {
  // Extract Bearer token from curl command
  const match = curlCommand.match(/['"](Bearer [^'"]+)['"]/);
  if (match) {
    capturedAuth = { authorization: match[1] };
    console.log('✅ Auth extracted from cURL');
    return capturedAuth;
  }
  console.error('❌ Could not find Bearer token in cURL command');
  return null;
}

async function fetchNewLikes() {
  const baseUrl = 'https://sora.chatgpt.com/backend/project_y/profile/user-04PG8OINU0U6an381AX3Fu51/post_listing/likes';
  
  // Check for auth
  if (!capturedAuth) {
    console.error('❌ No auth set. Run captureAuth() first, or setAuth("Bearer YOUR_TOKEN")');
    return [];
  }
  
  // Load existing processed IDs
  let processedIds = new Set();
  try {
    const stored = localStorage.getItem('processedVideoIds');
    if (stored) {
      processedIds = new Set(JSON.parse(stored));
      console.log(`📋 Loaded ${processedIds.size} existing video IDs`);
    }
  } catch (e) {
    console.warn('No existing video IDs found in localStorage');
  }
  
  const newItems = [];
  let cursor = null;
  let pageNum = 0;
  let hitExisting = false;
  
  while (!hitExisting) {
    pageNum++;
    const url = cursor 
      ? `${baseUrl}?cursor=${encodeURIComponent(cursor)}&limit=50`
      : `${baseUrl}?limit=50`;
    
    console.log(`📥 Fetching page ${pageNum}...`);
    
    const response = await fetch(url, { 
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
        ...capturedAuth
      }
    });
    
    if (!response.ok) {
      console.error(`❌ Error: ${response.status}`);
      break;
    }
    
    const data = await response.json();
    
    if (data.items && data.items.length > 0) {
      let newOnThisPage = 0;
      
      for (const item of data.items) {
        const videoId = item.post?.attachments?.[0]?.video_id || 
                       item.post?.id?.replace('s_', '') ||
                       item.post_id?.replace('s_', '');
        
        if (processedIds.has(videoId)) {
          console.log(`🛑 Hit existing video: ${videoId}`);
          hitExisting = true;
          break;
        }
        
        newItems.push(item);
        newOnThisPage++;
      }
      
      console.log(`   Page ${pageNum}: ${newOnThisPage} new items (Total new: ${newItems.length})`);
    }
    
    if (!hitExisting && data.cursor) {
      cursor = data.cursor;
    } else if (!data.cursor) {
      console.log('📄 Reached end of likes');
      break;
    }
    
    // Rate limiting
    await new Promise(r => setTimeout(r, 300));
  }
  
  // Store results
  window.newSoraLikes = newItems;
  
  if (newItems.length > 0) {
    // Also save to localStorage for easy export
    localStorage.setItem('newSoraLikes', JSON.stringify(newItems));
    localStorage.setItem('newLikesFetchedAt', new Date().toISOString());
    
    console.log(`\n✅ Found ${newItems.length} NEW liked videos!`);
    console.log(`📋 Access via: window.newSoraLikes`);
    console.log(`💾 Also saved to localStorage['newSoraLikes']`);
    console.log(`\n📝 To export, run: copy(JSON.stringify(window.newSoraLikes, null, 2))`);
  } else {
    console.log(`\n✅ No new likes since last sync!`);
  }
  
  return newItems;
}

/**
 * Helper: Load existing IDs from your sora_likes_enhanced.json using file picker
 * 
 * Usage: Run loadExistingIdsFromFile() and select your sora_likes_enhanced.json
 */
async function loadExistingIdsFromFile() {
  return new Promise((resolve) => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    
    input.onchange = async (e) => {
      const file = e.target.files[0];
      const text = await file.text();
      const data = JSON.parse(text);
      
      // Handle both array format and {videos: [...]} format
      const videos = Array.isArray(data) ? data : (data.videos || []);
      const ids = videos.map(v => v.videoId || v.video_id).filter(Boolean);
      
      localStorage.setItem('processedVideoIds', JSON.stringify(ids));
      console.log(`✅ Loaded ${ids.length} video IDs into localStorage`);
      resolve(ids);
    };
    
    input.click();
  });
}

/**
 * Helper: Load existing IDs from pasted JSON data
 * 
 * Usage: loadExistingIds(YOUR_PASTED_JSON)
 */
function loadExistingIds(soraLikesData) {
  const videos = Array.isArray(soraLikesData) ? soraLikesData : (soraLikesData.videos || []);
  const ids = videos.map(v => v.videoId || v.video_id).filter(Boolean);
  localStorage.setItem('processedVideoIds', JSON.stringify(ids));
  console.log(`✅ Loaded ${ids.length} video IDs into localStorage`);
  return ids;
}

/**
 * Helper: Update processed IDs after running analysis
 * Call this after you've processed new videos
 */
function markAsProcessed(videoIds) {
  let existing = [];
  try {
    existing = JSON.parse(localStorage.getItem('processedVideoIds') || '[]');
  } catch (e) {}
  
  const updated = [...new Set([...existing, ...videoIds])];
  localStorage.setItem('processedVideoIds', JSON.stringify(updated));
  console.log(`✅ Marked ${videoIds.length} videos as processed (Total: ${updated.length})`);
}

// Instructions
console.log('🎬 Sora New Likes Fetcher');
console.log('========================');
console.log('');
console.log('STEP 1: Load existing video IDs');
console.log('  → await loadExistingIdsFromFile()');
console.log('');
console.log('STEP 2: Set auth token');
console.log('  → Go to Network tab, find any backend request');
console.log('  → Copy the Authorization header value');
console.log('  → Run: setAuth("Bearer ey...")');
console.log('');
console.log('STEP 3: Fetch new likes');
console.log('  → await fetchNewLikes()');
console.log('');
console.log('STEP 4: Export');
console.log('  → copy(JSON.stringify(window.newSoraLikes, null, 2))');
console.log('');
console.log('Start with: await loadExistingIdsFromFile()');

