def type_file(file_received):
    file_received = file_received.split(".")

    archive = file_received[-1].lower()

    if archive == 'jpeg' or archive == 'png' or archive == 'jpg' or archive == 'jpe':

        extension_type = 1

    elif archive == 'docx' or archive == 'doc':
        extension_type = 2

    elif archive == 'pdf':
        extension_type = 3

    elif archive == 'xlsx' or archive == 'xls' or archive == 'csv':
        extension_type = 4

    elif archive == 'pptx' or archive == 'ppt':
        extension_type = 5

    elif archive == 'mp3' or archive == 'ogg' or archive == 'wma' or archive == 'pcm' or archive == 'wav':
        extension_type = 6

    elif archive == 'avi' or archive == 'mov' or archive == 'wmv' or archive == 'mp4' or archive == 'flv' or archive == 'mkv' or archive == 'rm' or archive == '3gp':
        extension_type = 7

    else:
        extension_type = 0

    return extension_type


def type_file_ext(file_received):
    file_received = file_received.split(".")

    archive = file_received[-1].lower()

    return archive
