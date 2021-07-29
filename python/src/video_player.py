"""A video player class."""
from video_library import VideoLibrary
from random import choice
from video_playlist import Playlist


class VideoPlayer:
	"""A class used to represent a Video Player."""

	def __init__(self):
		self._video_library = VideoLibrary()
		self.isPaused = False
		self.isPlaying = False
		self._current_video = None
		self._random_video = None
		self._status = False
		self._playlists = {}
		self._searchvideos = {}
		self.isVideo = False
		self.isflaged = False
		self.videoflaged = {}
		self._current_video_id = None
		self.countvideo = {}
		self.count = 0
		self.numberofvideos = None
		self._currentplaylists = []
		self.ratedvideos = {}

	def number_of_videos(self):
		num_videos = len(self._video_library.get_all_videos())
		print(f"{num_videos} videos in the library")

	def show_all_videos(self):
		"""Returns all videos."""
		videos_list = self._video_library.get_all_videos()
		videos_list.sort(key=lambda x: x.title)
		print("Here's a list of all available videos:")
		for videos in videos_list:
			tagString = " ".join(videos.tags)
			if videos.title in self.videoflaged:
				print(f"{videos.title} ({videos.video_id}) [{tagString}] - FLAGGED (reason: {self.videoflaged[videos.title]})")
			else:
				tagString = " ".join(videos.tags)
				print(f'{videos.title} ({videos.video_id}) [{tagString}]')

	def play_video(self,video_id):
		video = self._video_library.get_video(video_id)
		self.isPaused = False
		if not video:
			print("Cannot play video: Video does not exist")
			return
		elif self._current_video != None:
			print(f"Stopping video: {self._current_video}")
			print(f"Playing video: {video.title}")
			self._current_video = video.title
			self._status = True
			return

		elif video.title in self.videoflaged:
			print(f"Cannot play video: Video is currently flagged (reason: {self.videoflaged[video.title]})")

		else:
			print(f"Playing video: {video.title}")
			self._current_video = video.title



	def stop_video(self):
		current_video = self._current_video
		if current_video:
			print(f"Stopping video: {self._current_video}")
			self._current_video = None
		else:
			print("Cannot stop video: No video is currently playing")


	def play_random_video(self):
		list_video = [item for item in self._video_library.get_all_videos() if item.title not in self.videoflaged]
		try:
			random_video = choice(list_video)
			if not random_video:
				print("No videos available")
				return
			elif self._current_video != None:
				print(f"Stopping video: {self._current_video}")
				print(f"Playing video: {random_video.title}")
				self._current_video = random_video.title
				return
			else:
				print(f"Playing video: {random_video.title}")
				self._current_video = random_video.title
		except IndexError:
			print("No videos available")


	def pause_video(self):
		if self._current_video is None:
			print("Cannot pause video: No video is currently playing")
			return
		if self.isPaused and not self._status:
			print(f"Video already paused: {self._current_video}")
			return
		print(f"Pausing video: {self._current_video}")
		self.isPaused = True

	def continue_video(self):
		if self.isPaused:
			print(f"Continuing video: {self._current_video}")
			self.isPaused = False
			return
		elif self._current_video is None:
			print("Cannot continue video: No video is currently playing")
		else:
			print("Cannot continue video: Video is not paused")

	def show_playing(self):
		videos_list = self._video_library.get_all_videos()
		for videos in videos_list:
			tagString = " ".join(videos.tags)
			if self._current_video == videos.title and self.isPaused:
				print(f"Currently playing: {videos.title} ({videos.video_id}) [{tagString}] - PAUSED")
				return
			if self._current_video == videos.title and not self.isPaused:
				print(f"Currently playing: {videos.title} ({videos.video_id}) [{tagString}]")

		if self._current_video is None:
			print("No video is currently playing")

	def create_playlist(self, playlist_name):
		"""Creates a playlist with a given name.
		Args:
			playlist_name: The playlist name.
		"""
		if playlist_name.lower() in self._playlists:
			print("Cannot create playlist: A playlist with the same name already exists")
			return
		print(f"Would you like to create new playlist, {playlist_name}?")
		answer = input()
		if answer.upper() == "Y" or "YES":
			print(f"Successfully created new playlist: {playlist_name}")
			self._playlists[playlist_name.lower()] = Playlist(playlist_name)
		else:
			return

	def add_to_playlist(self, playlist_name, video_id,flag_reason="Not supplied"):
		video = self._video_library.get_video(video_id)
		if playlist_name.lower() not in self._playlists:
			print(f"Cannot add video to {playlist_name}: Playlist does not exist")
			return

		elif not video:
			print(f"Cannot add video to {playlist_name}: Video does not exist")
			return

		playlist = self._playlists[playlist_name.lower()]
		if video in playlist.video:
			print(f"Cannot add video to {playlist_name}: Video already added")
			return

		if video.title in self.videoflaged:
			print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {flag_reason})")
			return

		playlist.video.append(self._video_library.get_video(video_id))
		print(f"Added video to {playlist_name}: {video.title}")
		self.count+=1
		self.countvideo[playlist_name.lower()] = self.count

	def play_playlist(self,playlist_name):
		if playlist_name.lower() in self._playlists:
			print(f"Playing playlist, {playlist_name}")
			self._currentplaylists.append(playlist_name)
		else:
			print("Cannot play playlist. Playlist does not exist")

	def show_current_playlists(self):
		if not self._currentplaylists:
			print("No playlist is currently playing")
			return
		for playlist in sorted(self._currentplaylists):
			print(playlist)


	def show_all_playlists(self):
		"""Display all playlists."""
		if not self._playlists:
			print("No playlists exist yet")
			return
		print(f"Showing all playlists:")
		for playlist in sorted(self._playlists):
			if self.countvideo[playlist.lower()] == 1:
				self.numberofvideos = "1 video"
			else:
				self.numberofvideos = f"{self.countvideo[playlist.lower()]} videos"
			print(f"{self._playlists[playlist].name}({self.numberofvideos})")

	def show_playlist(self, playlist_name):
		if playlist_name.lower() not in self._playlists:
			print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
			return

		playlist = self._playlists[playlist_name.lower()]
		if self.countvideo[playlist_name.lower()] == 1:
			self.numberofvideos = "1 video"
		else:
			self.numberofvideos = f"{self.countvideo[playlist_name.lower()]} videos"

		print(f"Showing playlist: {playlist_name}({self.numberofvideos})")
		if not playlist.video:
			print("No videos here yet")
		else:
			for videos in playlist.video:
				tagString = " ".join(videos.tags)
				if videos.title in self.videoflaged:
					print(f"{videos.title} ({videos.video_id}) [{tagString}] - FLAGGED (reason: {self.videoflaged[videos.title]})")
				else:
					tagString = " ".join(videos.tags)
					print(f'{videos.title} ({videos.video_id}) [{tagString}]')

	def remove_from_playlist(self, playlist_name, video_id):
		video = self._video_library.get_video(video_id)
		if playlist_name.lower() not in self._playlists:
			print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
			return

		elif not video:
			print(f"Cannot remove video from {playlist_name}: Video does not exist")
			return

		playlist = self._playlists[playlist_name.lower()]

		if video in playlist.video:
			playlist.video.remove(video)
			print(f"Removed video from {playlist_name}: {video.title}")
			return

		if video not in playlist.video:
			print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
			return

	def clear_playlist(self, playlist_name):
		if playlist_name.lower() not in self._playlists:
			print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
			return
		playlist = self._playlists[playlist_name.lower()]
		if playlist.video:
			playlist.video.clear()
			print(f"Successfully removed all videos from {playlist_name}")

	def delete_playlist(self, playlist_name):
		if playlist_name.lower() not in self._playlists:
			print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
			return
		else:
			self._playlists.pop(playlist_name)
			print(f"Deleted playlist: {playlist_name}")

	def output_search_results(self, results, value):
		if not results:
			print(f"No search results for {value}")
			return
		print(f"Here are the results for {value}:")
		count = 0
		for i, result in enumerate(results):
			tagString = " ".join(result.tags)
			print(f'{i+1}) {result.title} ({result.video_id}) [{tagString}]')
			count = count+1
			self._searchvideos[count]=result.title
		print("Would you like to play any of the above? If yes, specify the number of the video.")
		print("If your answer is not a valid number, we will assume it's a no.")
		num = input()
		if num.isnumeric():
			for keys in self._searchvideos:
				if keys is int(num):
					print(f"Playing video: {self._searchvideos[keys]}")


	def search_videos(self, search_term):
		results = []
		videos_list = self._video_library.get_all_videos()
		videos_list.sort(key=lambda x: x.title)
		for videos in videos_list:
			if search_term.lower() in videos.title.lower() and videos.title not in self.videoflaged:
				results.append(videos)
		self.output_search_results(results,search_term)

	def search_videos_tag(self, video_tag):
		results = []
		videos_list = self._video_library.get_all_videos()
		videos_list.sort(key=lambda x: x.title)
		for videos in videos_list:
			tagString = "".join(videos.tags)
			if video_tag.lower() in tagString and videos.title not in self.videoflaged:
				results.append(videos)
		self.output_search_results(results,video_tag)

	def flag_video(self, video_id, flag_reason="Not supplied"):
		video = self._video_library.get_video(video_id)
		if not video:
			print("Cannot flag video: Video does not exist")
			return

		if video.title in self.videoflaged and self.isflaged:
			print("Cannot flag video: Video is already flagged")
			self.isflaged = False
			return
		current_video = self._current_video
		if current_video is video.title:
			print(f"Stopping video: {self._current_video}")
			self._current_video = None
		print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")
		self.videoflaged[video.title] = flag_reason
		self.isflaged = True

	def rate_video(self,video_id,rating):
		video = self._video_library.get_video(video_id)
		if not video:
			print("Cannot rate video: Video does not exist")
			return
		elif not rating.isnumeric() or int(rating)>5 or int(rating)<=0:
			print("Rating out of bound")
			return
		elif video.title in self.ratedvideos:
			print("Cannot rate video. Video already exists")
		elif rating in self.ratedvideos.values():
			print("Sorry. This rating already exists. Let's try again.")
		else:
			print(f"{video.title} has a rating of {rating}")
			self.ratedvideos[video.title] = rating

		for key,value in sorted(self.ratedvideos.items(),key=lambda kv:kv[1],reverse = True):
			print(value + " " + key)

	def undo_video(self,video_id):
		video = self._video_library.get_video(video_id)
		if video.title in self.ratedvideos:
			del self.ratedvideos[video.title]

	def allow_video(self, video_id):
		video = self._video_library.get_video(video_id)

		if not video:
			print("Cannot remove flag from video: Video does not exist")
			return

		if video.title not in self.videoflaged:
			print("Cannot remove flag from video: Video is not flagged")
			return

		print(f"Successfully removed flag from video: {video.title}")
		del self.videoflaged[video.title]


