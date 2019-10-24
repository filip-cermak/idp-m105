import time

def get_framerate(has_already_started,
				  start_time,
				  frame_counter,
				  frame_rate,
				  frame_num=5,
				  decimal_round_num=2):
	""" Returns current framerate of video based on
	time elapsed in frame_num frames.

	Works in a while loop for each frame"""
	if has_already_started:
		if frame_counter % 5 == 0:
			curr_time = time.time()
			frame_rate = frame_counter/(curr_time - start_time)
			frame_rate = round(frame_rate, decimal_round_num)
		frame_counter += 1
		return has_already_started, start_time, frame_counter, frame_rate


	else:
		has_already_started = True
		start_time = time.time()
		frame_counter = 0
		frame_rate = 0

		return has_already_started, start_time, frame_counter, frame_rate



"""
	try:
		framerate_getting_started = 
		if frame_counter % 5 == 0:
			try:
				curr_time = time.time()
				fps = frame_counter/(curr_time - start_time)
			except NameError as e:
				raise e
			start_time = time.time()

		frame_counter += 1
			
	except NameError as e:
		frame_counter = 0
		"""
