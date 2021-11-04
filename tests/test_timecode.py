import pytest
import timecode


def test_SMPTE_2997_DF_to_frames():

    frames = timecode.SMPTE_2997_DF_to_frames('01:00:00;00')
    assert frames == 107892

def test_SMPTE_2997_NDF_to_frames():
    frames = timecode.SMPTE_2997_NDF_to_frames('01:00:00:00')
    assert frames == 108000

def test_SMPTE_2398_to_frames():
    frames = timecode.SMPTE_2398_to_frames('01:00:00:00')
    assert frames == 86400

def test_SMPTE_25_to_frames():
    frames = timecode.SMPTE_25_to_frames('01:00:00:00')
    assert frames == 90000

def test_frames_to_file_relative_seconds():
    frames_2997ndf = 108000
    frames_2997df = 107892
    frames_2398 = 86400
    frames_25 = 90000

    frs_2997ndf = timecode.frames_to_file_relative_seconds('29.97', frames_2997ndf)
    frs_2997df = timecode.frames_to_file_relative_seconds('29.97', frames_2997df)
    frs_2398 = timecode.frames_to_file_relative_seconds('23.98', frames_2398)
    frs_25 = timecode.frames_to_file_relative_seconds('25', frames_25)

    assert frs_2997ndf == 3603.60
    assert frs_2997df == 3600.00
    assert frs_2398 == 3603.60
    assert frs_25 == 3603.60

def test_SMPTE_2997DF_clip():
    startTimecode = '00:59:59;00'
    endTimecode = '01:59:59;00'

    clip = timecode.SMPTE_2997DF_clip(startTimecode, endTimecode)
    assert clip.get('clip_duration') == 107892
    #todo - confirm in and outs are accurate

def test_SMPTE_2997NDF_clip():
    startTimecode = '00:59:59:00'
    endTimecode = '01:59:59:00'

    clip = timecode.SMPTE_2997NDF_clip(startTimecode, endTimecode)
    assert clip.get('clip_duration') == 108000
    # todo - confirm in and outs are accurate

def test_SMPTE_2398_clip():
    startTimecode = '00:59:59:00'
    endTimecode = '01:59:59:00'

    clip = timecode.SMPTE_2398_clip(startTimecode, endTimecode)
    assert clip.get('clip_duration') == 86400
    # todo - confirm in and outs are accurate

def test_SMPTE_25_clip():
    startTimecode = '00:59:59:00'
    endTimecode = '01:59:59:00'

    clip = timecode.SMPTE_25_clip(startTimecode, endTimecode)
    assert clip.get('clip_duration') == 90000
    # todo - confirm in and outs are accurate
