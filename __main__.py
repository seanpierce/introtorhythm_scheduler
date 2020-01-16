"""
The stream generator module is reponsible for collecing the current scheduled show, 
then creating an ezstream config file, replacing any current processes along the way.
"""

import os
import glob
import datetime
import xml.etree.ElementTree as XML
import requests
import config


def get_show():
    """
    Calls the scheduling API to retrieve the currently scheduled show.
    """

    if bool(config.DEBUG): 
        return {
            'day': datetime.datetime.now().weekday(),
            'start_time': datetime.datetime.now().hour,
            'title': 'Test Show',
            'audio': 'test_song.mp3'
        }

    url = "%s/api/schedule/show" %config.HOST
    return requests.get(url).json()


def delete_existing_config():
    """
    Returns a boolean value depending on the presence of the ezstream config file.
    Writes the outcome to a log file prior to returning.
    """

    config_list = glob.glob("%s/scheduler.xml" %os.path.dirname(os.path.abspath(__file__)))
    pid_list = glob.glob("%s/pid.txt" %os.path.dirname(os.path.abspath(__file__)))

    if len(config_list) > 0:
        os.remove(config_list[0])

    if len(pid_list) > 0:
        # read pid from file
        with open("%s/pid.txt" %os.path.dirname(os.path.abspath(__file__))) as file:
            pid = file.readline().strip()
            # kill process (if exists)
            # note: ezstream process will always be 1 more than the pid on file
            os.system("kill -9 %s" %(int(pid) + 1))

        # delete file
        os.remove(pid_list[0])


def create_ezstream_config(filename):
    """
    Creates ezstream xml config file
    """

    # create the file structure
    ezstream = XML.Element('ezstream')
    url_element = XML.SubElement(ezstream, 'url')
    sourcepassword = XML.SubElement(ezstream, 'sourcepassword')
    format_element = XML.SubElement(ezstream, 'format')
    filename_element = XML.SubElement(ezstream, 'filename')
    svrinfoname = XML.SubElement(ezstream, 'svrinfoname')
    svrinfourl = XML.SubElement(ezstream, 'svrinfourl')
    svrinfogenre = XML.SubElement(ezstream, 'svrinfogenre')
    svrinfodescription = XML.SubElement(ezstream, 'svrinfodescription')
    svrinfobitrate = XML.SubElement(ezstream, 'svrinfobitrate')
    svrinfochannels = XML.SubElement(ezstream, 'svrinfochannels')
    svrinfosamplerate = XML.SubElement(ezstream, 'svrinfosamplerate')
    svrinfopublic = XML.SubElement(ezstream, 'svrinfopublic')
    stream_once = XML.SubElement(ezstream, 'stream_once')

    # populate element values
    url_element.text = config.STREAM_URL
    sourcepassword.text = config.STREAM_PASSWORD
    format_element.text = 'MP3'
    filename_element.text = "%s/%s" %(config.UPLOAD_DIR, filename)
    svrinfoname.text = 'Intro To Rhythm'
    svrinfourl.text = 'https://introtorhythm.com'
    svrinfogenre.text = 'Electronic, Club, Funk, Post Punk, Techno, House, Avant Garde, Ambient'
    svrinfodescription.text = 'ITR is a free-form mix series and live audio-streaming station.'
    svrinfobitrate.text = '16'
    svrinfochannels.text = '1'
    svrinfosamplerate.text = '22050'
    svrinfopublic.text = '1'
    stream_once.text = '1'

    # write file
    ezstream_config = XML.tostring(ezstream)
    path = "%s/scheduler.xml" %os.path.dirname(os.path.abspath(__file__))
    ezstream_config_file = open(path, "wb")
    ezstream_config_file.write(ezstream_config)


def start_ezstream():
    """
    Compiles a command to execute an ezstream process.
    Saves the process id (pid) to a file for furure reference.
    """

    path_to_config = "%s/scheduler.xml" %os.path.dirname(os.path.abspath(__file__))
    path_to_pid = "%s/pid.txt" %os.path.dirname(os.path.abspath(__file__))
    command = "sh -c 'echo $$ > %s; ezstream -c %s'" %(path_to_pid, path_to_config)
    os.system(command)


if __name__ == "__main__":
    SHOW = get_show()

    if SHOW is None:
        print('No show')
        raise SystemExit(0)

    delete_existing_config()
    create_ezstream_config(SHOW['audio'])
    start_ezstream()