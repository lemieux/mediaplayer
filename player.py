import os
import sys
import pygame
pygame.init()


class MediaPlayer:
    def __init__(self, path):
        self.base_path = os.path.abspath(path)
        self.current_path = self.base_path
        self.paused = False

    def start(self):
        self.prompt_menu()

    def prompt_menu(self):
        self.directories = [name for name in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, name))]
        self.files = [name for name in os.listdir(self.current_path) if not os.path.isdir(os.path.join(self.current_path, name)) \
                        and (name.endswith("wav") or name.endswith("mp3") or name.endswith("flac"))]

        self.is_top = is_top = self.current_path == self.base_path
        contains_files = len(self.files) > 0
        contains_directories = len(self.directories) > 0

        if contains_files and contains_directories:
            print "Do you want to play files or search directories in this folder?"
            print "1. Play files"
            print "2. Search directories"
            if not is_top:
                print "b. Go back"
                print "t. Go to top level"
            print "x. Exit"
            completed = False
            while not completed:
                input = raw_input("> ")
                try:
                    input = int(input)
                    if input in [1, 2, "b", "t", "x"] and is_top or input in [1, 2, "x"] and not is_top:
                        completed = True
                        if input == 1:
                            self.prompt_files_menu()
                        elif input == 2:
                            self.prompt_directories_menu()
                        elif input == "b":
                            self.go_up()
                        elif input == "x":
                            exit()
                        else:
                            self.go_top()
                except:
                    pass
                if not completed:
                    print "Wrong value. Please selected a valid choice."

        elif contains_directories and not contains_files:
            self.prompt_directories_menu()
        elif contains_files and not contains_directories:
            self.prompt_files_menu()
        elif not is_top:
            print "This directory is empty. We're goind back up a level."
            self.go_up()
        else:
            print "Your media folder is empty. Exiting now."

    def go_up(self):
        self.current_path = os.path.abspath(os.path.join(self.current_path, '..'))
        self.prompt_menu()

    def go_top(self):
        self.current_path = self.base_path
        self.prompt_menu()

    def prompt_files_menu(self):
        print "This folder has %s file%s in it. What do you want to do?" % (len(self.files), "s" if len(self.files) > 1 else "")
        print "1. Play them all"
        print "2. Shuffle them then play them all"
        print "3. I'll pick one"
        if not self.is_top:
            print "b. Go back"
            print "t. Go to top level"
        print "x. Exit"
        completed = False
        while not completed:
            input = raw_input("> ")
            if input in ["1", "2", "3", "b", "t", "x"] and not self.is_top or self.is_top and input in ["1", "2", "3", "x"]:
                completed = True
                if input == "1":
                    self.play_files()
                    self.prompt_menu()
                elif input == "2":
                    self.play_files(shuffle=True)
                    self.prompt_menu()
                elif input == "3":
                    song = self.prompt_file_chooser()
                    if song is not None:
                        self.play_file(song)
                    else:
                        completed = False
                    self.prompt_menu()
                elif input == "b":
                    self.go_up()
                elif input == "x":
                    exit()
                else:
                    self.go_top()
            else:
                print "Wrong value. Please select a valid choice."

    def prompt_file_chooser(self):
        print "Please choose from the following list :"
        for i, song in enumerate(self.files):
            print "%s. %s" % (i + 1, song)
        print "c. Cancel"
        completed = False
        while not completed:
            input = raw_input("> ")
            if input == 'c':
                return None
            try:
                input = int(input)
                if input > 0 and input <= len(self.files):
                    completed = True
                    return self.files[input - 1]
            except:
                pass
            if not completed:
                print "Wrong value. Please select a valid choice."

    def prompt_directories_menu(self):
        print "Which directory do you want to search?"
        for i, name in enumerate(self.directories):
            print "%s. %s" % (i + 1, name)
        if not self.is_top:
            print "b. Go back"
            print "t. Go to top level"
        print "x. Exit"
        completed = False
        while not completed:
            input = raw_input("> ")
            if input == "b":
                self.go_up()
            elif input == "t":
                self.go_top()
            elif input == "x":
                exit()
            else:
                try:
                    input = int(input)
                    if input > 0 and input <= len(self.directories):
                        completed = True
                        self.current_path = os.path.join(self.current_path, self.directories[input - 1])
                        self.prompt_menu()
                except:
                    pass
            if not completed:
                print "Wrong value. Please select a valid choice."

    def play_files(self, shuffle=False):
        files = self.files
        if shuffle:
            from random import shuffle as random_shuffle
            random_shuffle(files)
        for file in files:
            self.play_file(file)

    def play_file(self, song):
        print "Now playing : %s" % song
        pygame.mixer.music.load(os.path.abspath(os.path.join(self.current_path, song)))
        pygame.mixer.music.play()
        self.prompt_music_menu()

    def prompt_music_menu(self):
        while pygame.mixer.music.get_busy():
            print "What you want to do?"
            print "1. Stop"
            print "2. Skip"
            print "x. Exit"
            input = raw_input("> ")
            while input not in ["1", "2", "x"]:
                print "Wrong value. Please select a valid choice."
            if input == "1" or input == "x" or input == "2":
                pygame.mixer.music.stop()
            if input == "x":
                exit()

if __name__ == '__main__':
    print 'Media player v0.1'
    if len(sys.argv) != 2 or (len(sys.argv) == 2 and sys.argv[1] == ''):
        print 'Usage python player.py [path_to_music_folder]'
    else:
        path = sys.argv[1]
        if not os.path.exists:
            print "The provided path doesn't exists."
        else:
            player = MediaPlayer(path)
            try:
                player.start()
            except Exception as error:
                print error
