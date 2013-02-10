import os
import logging
from subprocess import check_output
from pprint import pprint
from tempfile import mkdtemp, gettempdir

logger = logging.getLogger(__name__)
logging.basicConfig()


class FlagError(Exception):
    pass


class ExtractionError(Exception):
    pass

#============================COMPRESSION SWITCHES=============================#


def flg_output(location=os.curdir):
    if not os.path.isdir(location):
        raise FlagError("Invalid Path Location Specified")
    return (r"-o%s" % (location))


def flg_suppress(sup=True):
    if not isinstance(sup, bool):
        raise FlagError("Suppress Requires a boolean response")
    return "-y" if sup == True else ""


def flg_compression(level="x9"):
    if level not in ["x9", "x7", "x5", "x3", "x1", "x0", "mt"]:
        raise FlagError("Invalid compression level")
    return "-m%" % (level)


def flg_format(ext="7z"):
    if ext not in ("7z", "rar", "zip", "gzip", "ttar", "tiso", "tudf"):
        raise FlagError("%s is not a supported file format" % ext)
    return "-t%s" % (ext)


def flg_solid(on=True):

    if not isinstance(on, bool):
        raise FlagError("Solid Requires a boolean Argument")
    if on == True:
        return "-ms=on"
    else:
        return "-ms=off"


def flg_password(password):
    if not isinstance(password, str):
        raise FlagError("A valid password must be provided")
    return "-p%s" % (password)


def flg_recurse(rec=True):
    if rec == True:
        return "-r"
    else:
        return ""

#===============================7Z METHODS==================================#
def temp_extract(inputting, files = None):
    temp_directory = mkdtemp()
    temp_directory = os.path.normpath(temp_directory)
     
    return extract(inputting, out = temp_directory, files = files)
    
def extract(inputting, out=os.curdir, files=None, full_paths=False):
    command = ["7za\\7za.exe", flg_suppress(), flg_output(out), "e", inputting]
    
    if full_paths == True:
        command[-2] = "x"
        del command[-3]
    if files != None:
        command.append(files)

    output = check_output(command)
    output = output.split("\r\n")

    results = output[5:-7]
    results.append(output[-6])

    for extract in results:
        logging.info(extract)

    #We now need to return the file list
    results = [each.split(" ", 1)[1].strip(" ") for each in output[5:-7]]
    results = [os.path.join(out, res) for res in results]

    return results


def list_archive(inputting):
    listed = check_output(["7za/7za.exe", "l", inputting])
    delimiter = "------------------- ----- ------------ ------------  ------------------------"
    file_list = listed.split(delimiter)[1]

    file_list = [line[53:].strip() for line in file_list.split("\n")][1:-1]

    return file_list


def delete(compressed, files=None):
    command = ["7za\\7za.exe", "-y", "d", compressed]
    if files != None:
        command.append(files)

    out = check_output(command)
    out = out.split("\r\n")[-2]
    logging.info(out)

    return out


def add(compressed, files):
    command = ["7za\\7za.exe", "-y", "a", compressed, files]
    out = check_output(command)
    out = out.split("\r\n")[-2]
    logging.info(out)

    return out


def test(compressed, files=None, recursive=True):
    command = ["7za\\7za.exe", "-y", "t", compressed]
    if not files == None:
        command.append("files")
    if recursive:
        command.append("-r")

    out = check_output(command)
    out = out.split("\r\n")
    logging.info(out)
    return out


