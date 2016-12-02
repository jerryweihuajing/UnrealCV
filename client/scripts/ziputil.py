import os
import ue4util
import zipfile

# Even empty folder needs to be preserved
def get_all_files(files, include_folder=True, verbose=False):
    '''
    Recursive expand folder and get all files in abspath format
    '''
    all_files = []
    for path in files:
        if verbose:
            print 'path: %s' % path

        if os.path.isfile(path) or include_folder:
            all_files.append(path)

        if os.path.isdir(path):
            for dirname, subdirs, files in os.walk(path):
                # print 'dirname: %s' % dirname
                # print 'subdirs: %s' % subdirs
                # print 'files: %s' % files
                for filename in files:
                    all_files.append(os.path.join(dirname, filename))

                for subdir in subdirs:
                    if include_folder:
                        all_files.append(os.path.join(dirname, subdir))

    return [ue4util.get_real_abspath(v) for v in all_files]

def zipfiles(srcfiles, srcroot, dst, verbose=False):
    '''
    srcfiles: files in abspath format
    srcroot: root will be subtracted for converting to relative path
    dst: zip file
    '''
    srcroot = ue4util.get_real_abspath(srcroot) # Make sure it has the same format as srcfiles
    print 'zip files %s ... to file %s, with root %s' % (srcfiles[0], dst, srcroot)
    zf = zipfile.ZipFile("%s" % (dst), "w", zipfile.ZIP_DEFLATED)

    for srcfile in srcfiles:
        # arcname = srcfile[len(srcroot) + 1:]
        arcname = srcfile.replace(srcroot, '').lstrip('/')
        # Make sure it is a relative path, absolute path is quite dangerous and might overwrite something 
        if verbose:
            print 'zipping %s as %s' % (srcfile,
                                        arcname)
        assert arcname == '' or arcname[0] != '/' # Make sure this is not staring from the root
        zf.write(srcfile, arcname)

    zf.close()
