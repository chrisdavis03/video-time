import re

def SMPTE_2997_DF_to_frames(tc):
	'''At 29.97 fps, every minute (except minutes divisible by ten), you skip counting the first two frames.'''
	hh, mm, ss, ff = re.split(':|;', tc)
	totalMinutes = 60 * int(hh) + int(mm)
	#Looking at the last part of this equation. We drop 2 frames every minute EXCEPT the ones divisible by 10.
	frameNumber = 108000 * int(hh) + 1800 * int(mm) + 30 * int(ss) + int(ff) - 2 * (totalMinutes - totalMinutes / 10)
	return int(frameNumber)

def SMPTE_2997_NDF_to_frames(tc):
	hh, mm, ss, ff = re.split(':', tc)
	frameNumber = 108000 * int(hh) + 1800 * int(mm) + 30 * int(ss) + int(ff)

	return int(frameNumber)

def SMPTE_2398_to_frames(tc):
	hh, mm, ss, ff = re.split(':', tc)
	frameNumber = 86400 * int(hh) + 1800 * int(mm) + 30 * int(ss) + int(ff)

	return int(frameNumber)

def frames_to_file_relative_seconds(framerate, frames):
	#At this point drop frame doesn't matter. Frames counts @ 29.97 are all the same duration.
	if framerate == '29.97':
		#id prefer to round to the nearest frame boundary but for now we are calling it 2 decimal places.
		file_relative_seconds = round((1/(30000/1001)) * frames, 2)
		return file_relative_seconds
	if framerate == '23.98':
		#id prefer to round to the nearest frame boundary but for now we are calling it 2 decimal places.
		file_relative_seconds = round((1/(24000/1001)) * frames, 2)
		return file_relative_seconds
	pass

def frames_to_SMPTE_2997_DF(frameNumber):
	frameNumber += 1
	D = frameNumber	/ 17982
	M = frameNumber % 17982
	frameNumber += 18 * D + 2 * ((M - 2) / 1798)
	#(If - 2 div 1798 doesn't return 0, you'll have to special-case M = 0 or 1.)
	ff = frameNumber % 30
	ss = (frameNumber / 30)	% 60
	mm = ((frameNumber / 30) / 60)	% 60
	hh = (((frameNumber / 30) / 60) / 60) % 24

	return '{}:{}:{};{}'.format('{:02d}'.format(int(hh)), '{:02d}'.format(int(mm)), '{:02d}'.format(int(ss)), '{:02d}'.format(int(ff)))

def SMPTE_2997DF_clip(tcIn, tcOut):
	startFrames = SMPTE_2997_DF_to_frames(tcIn)
	endFrames = SMPTE_2997_DF_to_frames(tcOut)

	clipDuration = endFrames - startFrames
	startFileRelativeSeconds = frames_to_file_relative_seconds('29.97', startFrames)
	endFileRelativeSeconds = frames_to_file_relative_seconds('29.97', endFrames)

	return {"clip_duration": clipDuration, "in_file_relative_seconds": startFileRelativeSeconds, "out_file_relative_seconds": endFileRelativeSeconds}

def SMPTE_2997NDF_clip(tcIn, tcOut):
	startFrames = SMPTE_2997_NDF_to_frames(tcIn)
	endFrames = SMPTE_2997_NDF_to_frames(tcOut)

	clipDuration = endFrames - startFrames
	startFileRelativeSeconds = frames_to_file_relative_seconds('29.97', startFrames)
	endFileRelativeSeconds = frames_to_file_relative_seconds('29.97', endFrames)

	return {"clip_duration": clipDuration, "in_file_relative_seconds": startFileRelativeSeconds, "out_file_relative_seconds": endFileRelativeSeconds}

def SMPTE_2398_clip(tcIn, tcOut):
	startFrames = SMPTE_2398_to_frames(tcIn)
	endFrames = SMPTE_2398_to_frames(tcOut)

	clipDuration = endFrames - startFrames
	startFileRelativeSeconds = frames_to_file_relative_seconds('23.98', startFrames)
	endFileRelativeSeconds = frames_to_file_relative_seconds('23.98', endFrames)

	return {"clip_duration": clipDuration, "in_file_relative_seconds": startFileRelativeSeconds, "out_file_relative_seconds": endFileRelativeSeconds}

if __name__ == '__main__':
	startTimecode = '00:59:59:00'
	endTimecode = '01:59:59:00'

	clip = SMPTE_2398_clip(startTimecode, endTimecode)
	print (clip)