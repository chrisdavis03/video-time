from openpyxl import load_workbook
import re
import os

class Timecode:
	def __init__(self, framerate):
		self.framerate = framerate
		self.dropframe = False

	def parse_tc(self, tc):
		hh, mm, ss, ff = re.split(':|;', tc)
		hh = int(hh)
		mm = int(mm)
		ss = int(ss)
		ff = int(ff)

		return hh, mm, ss, ff

	def set_dropframe(self, tc):
		if ';' in tc:
			self.dropframe == True
		else:
			self.dropframe == False

	def dftc_to_frames(self, tc):
		'''At 29.97 fps, every minute (except minutes divisible by ten), you skip counting the first two frames.'''
		hh, mm, ss, ff = re.split(':|;', tc)
		hh_sec = int(hh) * 3600
		mm_sec = int(mm) * 60
		ss_sec = int(ss)
		ff_sec = 1 / (30000 / 1001) * float(ff)

		totalMinutes = 60 * int(hh) + int(mm)
		#Looking at the last part of this equation. We drop 2 frames every minute EXCEPT the ones divisible by 10.
		frameNumber = 108000 * int(hh) + 1800 * int(mm) + 30 * int(ss) + int(ff) - 2 * (totalMinutes - totalMinutes / 10)
		#Looking at the last part of this equation. We drop 2 frames every minute EXCEPT the ones divisible by 10.
		return int(frameNumber)

	def frames_to_dftc(self, frameNumber):
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

	def list_to_delimited_string(self, source_list):
		'''Given a python list, return a pipe delimited string.'''
		# initializing delim
		delim = "|"
		res = ''
		for i in source_list:
			res = res + str(i) + delim

		return (res[:-1])

	def tc_to_seconds_2398(self, tc):
		try:
			hh, mm, ss, ff = tc.split(':')
			hh_sec = int(hh)*3600
			mm_sec = int(mm)*60
			ss_sec = int(ss)
			ff_sec = 1/(24000/1001)*float(ff)
			fileRelativeSecond = round((hh_sec + mm_sec + ss_sec + ff_sec), 2)
			return fileRelativeSecond
		except:
			return ''

	def tc_to_npt(self, tc):
		# print (tc)
		try:
			hh, mm, ss, ff = tc.split(':')
			ff_sec = 1/(24000/1001)*float(ff)
			fractional_seconds = round((int(ss) + float(ff_sec)), 2)
			fractional_seconds = '{:05.2f}'.format(fractional_seconds)
			#todo - ensure both ff_sec and frames are zero padded to 2 digits.
			normal_playTime = '{}:{}:{}'.format(hh, mm, fractional_seconds)
			return normal_playTime
		except:
			return ''

	def frames_to_fileRelativeSeconds(self, frames):
		fileRelativeSeconds = frames * (1/framerate)
		fileRelativeSeconds = round (fileRelativeSeconds, 3)
		return fileRelativeSeconds

if __name__ == '__main__':
	#todo - setup tests. this will get tedious.
	pass
	# framerate = 30000/1001
	# frames = dftc_to_frames('01:02:17;12')
	# frames_in = dftc_to_frames('00:01:00;00')
	# print (frames)
	# fileRelativeSeconds = frames_to_fileRelativeSeconds(frames, framerate)
	# print (fileRelativeSeconds)
	# print (fileRelativeSeconds/framerate)