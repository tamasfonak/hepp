import TokenRing

videos = {
	'floorLoop': '',
	'tableComesIn': '',
	'tableLoop': '',
	'tableGoesOut': ''
}

def compute_videos( starting = 0, total = 0 ):
	return ( starting, total )

TokenRing.token_sending.videos = compute_videos
TokenRing.start()
