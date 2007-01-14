import sys, os, string, re, commands, types

import SCons

# The following adds all SCons SConscript API to the globals of this module.
version = map(int,string.split(SCons.__version__,'.'))
if version[1] == 96 and version[2] >= 90:
    from SCons.Script import *
else:  # old style
    import SCons.Script.SConscript
    globals().update(SCons.Script.SConscript.BuildDefaultGlobals())

toheader = re.compile(r'\n((?:\n[^\n]+)+)\n'                     
                      '\s*\/\*(\^|\<(?:[^>]|\>[^*]|\>\*[^/])*\>)\*\/')
kandr = re.compile(r'\s*\{?\s*$') # K&R style function definitions end with {

def header(target=None,source=None,env=None):
# generate a header file
    inp = open(str(source[0]),'r')
    text = string.join(inp.readlines(),'')
    inp.close()
    file = str(target[0])
    prefix = env.get('prefix','')
    define = prefix + string.translate(os.path.basename(file),
                                       string.maketrans('.','_'))
    out = open(file,'w')
    out.write('/* This file is automatically generated. DO NOT EDIT! */\n\n')
    out.write('#ifndef _' + define + '\n')
    out.write('#define _' + define + '\n\n')
    for extract in toheader.findall(text):
        if extract[1] == '^':
            out.write(extract[0]+'\n\n')
        else:
            function = kandr.sub('',extract[0])
            out.write(function+';\n')
            out.write('/*'+extract[1]+'*/\n\n')
    out.write('#endif\n')
    out.close()
    return 0

Header = Builder (action = Action(header,varlist=['prefix']),
                  src_suffix='.c',suffix='.h')

include = re.compile(r'#include\s*\"([^\"]+)\.h\"')

def depends(env,list,file):
    filename = string.replace(env.File(file+'.c').abspath,'build/','',1)
    fd = open(filename,'r')
    for line in fd.readlines():
        for inc in include.findall(line):
            if inc not in list and inc[0] != '_':
                list.append(inc)
                depends(env,list,inc)
    fd.close()


include90 = re.compile(r'use\s+(\S+)')

def depends90(env,list,file):
    filename = string.replace(env.File(file+'.f90').abspath,'build/','',1)
    fd = open(filename,'r')
    for line in fd.readlines():
        for inc in include90.findall(line):
            if inc not in list and inc != 'rsf':
                list.append(inc)
                depends90(env,list,inc)
    fd.close()

def included(node,env,path):
    file = os.path.basename(str(node))
    file = re.sub('\.[^\.]+$','',file)
    contents = node.get_contents()
    includes = include.findall(contents)
    if file in includes:
        includes.remove(file)
    return map(lambda x: x + '.h',includes)

Include = Scanner(name='Include',function=included,skeys=['.c'])

def check_all(context):
    cc(context)
    ar(context)
    libs(context)
    c99(context)
    x11(context)
    ppm(context)
    jpeg(context)
    api = string.split(string.lower(context.env.get('API','')),',')
    if 'c++' in api:
        cxx(context)
    if 'fortran' in api:
        f77(context)
    if 'fortran-90' in api or 'fortran90' in api or 'f90' in api:
        f90(context)
    if 'python' in api:
	numpy(context)

def libs(context):
    context.Message("checking libraries ... ")
    LIBS = context.env.get('LIBS','m')
    if type(LIBS) is not types.ListType:
        LIBS = string.split(LIBS)
    if sys.platform[:5] == 'sunos':
        LIBS.append('nsl')
    elif sys.platform[:6] == 'cygwin':
        LIBS.append('rpc')
    elif sys.platform[:6] == 'darwin':
        LIBS.append('mx')
    elif sys.platform[:7] == 'interix':
        LIBS.append('rpclib')
    text = '''
    #include <rpc/types.h>
    #include <rpc/xdr.h>
    int main(int argc,char* argv[]) {
    return 0;
    }\n'''
    
    res = context.TryLink(text,'.c')
    if res:
        context.Result(str(LIBS))
        context.env['LIBS'] = LIBS
    else:
        context.Result(0)
        context.Message("Please install RPC libraries.\n")
        sys.exit(1)

xinc = [
    '/usr/X11/include',
    '/usr/X11R6/include',
    '/usr/X11R5/include',
    '/usr/X11R4/include',
    '/usr/include/X11',
    '/usr/include/X11R6',
    '/usr/include/X11R5',
    '/usr/include/X11R4',
    '/usr/local/X11/include',
    '/usr/local/X11R6/include',
    '/usr/local/X11R5/include',
    '/usr/local/X11R4/include',
    '/usr/local/include/X11',
    '/usr/local/include/X11R6',
    '/usr/local/include/X11R5',
    '/usr/local/include/X11R4',
    '/usr/X386/include',
    '/usr/x386/include',
    '/usr/XFree86/include/X11',
    '/usr/include',
    '/usr/local/include',
    '/usr/unsupported/include',
    '/usr/athena/include',
    '/usr/local/x11r5/include',
    '/usr/lpp/Xamples/include',
    '/usr/openwin/include',
    '/usr/openwin/share/include'
    ]

xlib = [
    '/usr/X11/lib',
    '/usr/X11R6/lib64',
    '/usr/X11R6/lib',
    '/usr/X11R5/lib',
    '/usr/X11R4/lib',
    '/usr/lib/X11',
    '/usr/lib/X11R6',
    '/usr/lib/X11R5',
    '/usr/lib/X11R4',
    '/usr/local/X11/lib',
    '/usr/local/X11R6/lib',
    '/usr/local/X11R5/lib',
    '/usr/local/X11R4/lib',
    '/usr/local/lib/X11',
    '/usr/local/lib/X11R6',
    '/usr/local/lib/X11R5',
    '/usr/local/lib/X11R4',
    '/usr/X386/lib',
    '/usr/x386/lib',
    '/usr/XFree86/lib/X11',
    '/usr/lib',
    '/usr/local/lib',
    '/usr/unsupported/lib',
    '/usr/athena/lib',
    '/usr/local/x11r5/lib',
    '/usr/lpp/Xamples/lib',
    '/lib/usr/lib/X11',
    '/usr/openwin/lib',
    '/usr/openwin/share/lib'
    ]

def x11(context):
    text = '''
    #include <X11/Intrinsic.h>
    #include <X11/Xaw/Label.h>
    int main(int argc,char* argv[]) {
    return 0;
    }\n'''
    
    context.Message("checking for X11 headers ... ")
    INC = context.env.get('XINC','')
    if type(INC) is not types.ListType:
        INC = string.split(INC)

    oldpath = context.env.get('CPPPATH',[])

    res = None
    for path in filter(lambda x:
                       os.path.isfile(os.path.join(x,'X11/Xaw/Label.h')),
                       INC+xinc):        
        context.env['CPPPATH'] = oldpath + [path,] 
        res = context.TryCompile(text,'.c')

        if res:
            context.Result(path)
            context.env['XINC'] = context.env['CPPPATH']
            break

    if not res:
        context.Result(0)
        context.env['XINC'] = None
        return

    context.Message("checking for X11 libraries ... ")
    LIB = context.env.get('XLIBPATH','')
    if type(LIB) is not types.ListType:
        LIB = string.split(LIB)

    oldlibpath = context.env.get('LIBPATH',[])
    oldlibs = context.env.get('LIBS',[])

    XLIBS = context.env.get('XLIBS')
    if XLIBS:
        if type(XLIBS) is not types.ListType:
            XLIBS = string.split(XLIBS)
    else:
        if  sys.platform[:7] == 'interix':
            XLIBS =  ['Xaw','Xt','Xmu','X11','Xext','SM','ICE']
        elif sys.platform[:5] == 'linux':
            XLIBS = ['Xaw','Xt']
        else:
            XLIBS = ['Xaw','Xt','X11']

    res = None
    for path in filter(os.path.isdir,LIB+xlib):        
        context.env['LIBPATH'] = oldlibpath + [path,] 
        res = context.TryLink(text,'.c')
        
        if res:
            context.Result(path)
            context.env['XLIBPATH'] = context.env['LIBPATH']
            context.env['XLIBS'] = XLIBS
            break
    if not res:
        context.Result(0)
        context.env['XLIBPATH'] = None

    context.env['CPPPATH'] = oldpath        
    context.env['LIBPATH'] = oldlibpath
    context.env['LIBS'] = oldlibs

def ppm(context):
    context.Message("checking ppm ... ")
    LIBS = context.env.get('LIBS','m')
    if type(LIBS) is not types.ListType:
        LIBS = string.split(LIBS)
    ppm = context.env.get('PPM','netpbm')
    LIBS.append(ppm)
    text = '''
    #include <ppm.h>
    int main(int argc,char* argv[]) {
    return 0;
    }\n'''
    
    res = context.TryLink(text,'.c')
    if res:
        context.Result(res)
        context.env['PPM'] = ppm
    else:
        context.Result(0)
        context.env['PPM'] = None

    LIBS.pop()

def jpeg(context):
    context.Message("checking jpeg ... ")
    LIBS = context.env.get('LIBS','m')
    if type(LIBS) is not types.ListType:
        LIBS = string.split(LIBS)
    jpeg = context.env.get('JPEG','jpeg')
    LIBS.append(jpeg)
    text = '''
    #include <stdio.h>
    #include <jpeglib.h>
    int main(int argc,char* argv[]) {
    return 0;
    }\n'''
    
    res = context.TryLink(text,'.c')
    if res:
        context.Result(res)
        context.env['JPEG'] = jpeg
    else:
        context.Result(0)
        context.env['JPEG'] = None

    LIBS.pop()


def ar(context):
    context.Message("checking ar ... ")
    AR = context.env.get('AR',WhereIs('ar'))
    if AR:
        context.Result(AR)
        context.env['AR'] = AR
    else:
        context.Result(0)
        sys.exit(1)

def cc(context):
    context.Message("checking C compiler ... ")
    CC = context.env.get('CC',WhereIs('gcc'))
    if CC:
        context.Result(CC)   
    else:
        context.Result(0)
        sys.exit(1)
    text = '''
    int main(int argc,char* argv[]) {
    return 0;
    }\n'''
    
    context.Message("checking if %s works ... " % CC)
    res = context.TryLink(text,'.c')
    context.Result(res)
    if not res:
        sys.exit(1)
    if CC[-3:]=='gcc':
        oldflag = context.env.get('CCFLAGS')
        for flag in ('-std=gnu99 -Wall -pedantic',
                     '-std=gnu9x -Wall -pedantic',
                     '-Wall -pedantic'):
            context.Message("checking if gcc accepts '%s' ... " % flag)
            context.env['CCFLAGS'] = oldflag + ' ' + flag
            res = context.TryCompile(text,'.c')
            context.Result(res)
            if res:
                break
        if not res:
            context.env['CCFLAGS'] = oldflag
        # large file support
        (status,lfs) = commands.getstatusoutput('getconf LFS_CFLAGS')
        if not status:
            oldflag = context.env.get('CCFLAGS')
            context.Message("checking if gcc accepts '%s' ... " % lfs)
            context.env['CCFLAGS'] = oldflag + ' ' + lfs
            res = context.TryCompile(text,'.c')
            context.Result(res)
            if not res:
                context.env['CCFLAGS'] = oldflag
    elif sys.platform[:5] == 'sunos':
        context.env['CCFLAGS'] = string.replace(context.env.get('CCFLAGS',''),
                                                '-O2','-xO2')

def c99(context):
    context.Message("checking complex support ... ")
    text = '''
    #include <complex.h>
    #include <math.h>
    int main(int argc,char* argv[]) {
    float complex c;
    float f;
    f = cabsf(ccosf(c));
    return (int) f;
    }\n'''

    res = context.TryLink(text,'.c')
    if res:
        context.Result(res)
    else:
        context.env['CCFLAGS'] = context.env.get('CCFLAGS','')+' -DNO_COMPLEX'
        context.Result(0)

def cxx(context):
    context.Message("checking C++ compiler ... ")
    CXX = context.env.get('CXX')
    if CXX:
        context.Result(CXX)   
    else:
        context.Result(0)
        return
    text = '''
    #include <valarray>
    int main(int argc,char* argv[]) {
    return 0;
    }\n'''

    context.Message("checking if %s works ... " % CXX)
    res = context.TryLink(text,'.cc')
    context.Result(res)
    if not res:
        del context.env['CXX']
        return
    if CXX == 'g++':
        oldflag = context.env.get('CXXFLAGS')
        for flag in ['-Wall -pedantic']:
            context.Message("checking if g++ accepts '%s' ... " % flag)
            context.env['CXXFLAGS'] = oldflag + ' ' + flag
            res = context.TryCompile(text,'.cc')
            context.Result(res)
            if res:
                break
        if not res:
            context.env['CXXFLAGS'] = oldflag

def numpy(context):
    context.Message("checking if numpy is present ... ")
    try:
	import numpy
	context.Result(1)
    except:
	context.Result(0)
	context.Message("checking if numarray is present ... ")
	try:
	    import numarray
	    context.Result(1)
	    context.Message("numarray development has stopped; plan to migrate to numpy")
	except:
	    context.Result(0)
	    sys.stderr.write("Please install numpy (preferred) or numarray.\n")
            sys.exit(1)

fortran = {'g77':'f2cFortran',
           'gfortran':'NAGf90Fortran', # used to be f2cFortran
           'f2c':'f2cFortran'}

def f77(context):
    context.Message("checking F77 compiler ... ")
    F77 = context.env.get('F77')
    if not F77:
        compilers = ['g77','f77','f90','f95','xlf90','pgf90',
                     'ifort','ifc','pghpf']
        F77 = context.env.Detect(compilers)
        if not F77:
            for comp in compilers:
                F77 = WhereIs(comp)
                if F77:
                    break
        context.env['F77'] = F77
    if F77:
        context.Result(F77)
    else:
        context.Result(0)
        return
    if os.path.basename(F77) == 'ifc' or os.path.basename(F77) == 'ifort':
        intel(context)
        context.env.Append(F77FLAGS=' -Vaxlib')
    text = '''      program Test
      stop
      end
      '''
    context.Message("checking if %s works ... " % F77)
    oldlink = context.env.get('LINK')
    context.env['LINK'] = F77
    res = context.TryLink(text,'.f')
    context.env['LINK'] = oldlink
    context.Result(res)
    if not res:
        sys.stderr.write("No working F77 compiler detected.\n")
        del context.env['F77']
        sys.exit(1)
    cfortran = fortran.get(os.path.basename(F77),'NAGf90Fortran')
    context.env['CFORTRAN'] = cfortran 
    context.Message("checking %s type for cfortran.h ... " % F77)
    context.Result(cfortran)

def f90(context):
    context.Message("checking F90 compiler ... ")
    F90 = context.env.get('F90')
    if not F90:
        compilers = ['gfortran','f90','f95','xlf90','pgf90',
                     'ifort','ifc','pghpf']
        F90 = context.env.Detect(compilers)
        if not F90:
            for comp in compilers:
                F90 = WhereIs(comp)
                if F90:
                    break
        context.env['F90'] = F90
    if F90:
        context.Result(F90)
    else:
        context.Result(0)
        return
    if os.path.basename(F90) == 'ifc' or os.path.basename(F90) == 'ifort':
        intel(context)
        context.env.Append(F90FLAGS=' -Vaxlib')
    main = '''program Test
    end program Test
    '''
    module = '''module testf90
    end module testf90
    '''
    context.Message("checking if %s works ... " % F90)
    oldlink = context.env.get('LINK')
    context.env['LINK'] = F90
    res1 = context.TryCompile(module,'.f90')
    res2 = context.TryLink(main,'.f90')
    context.env['LINK'] = oldlink
    context.Result(res1 and res2)
    if not res1 or not res2:
        sys.stderr.write("No working F90 compiler detected.\n")
        del context.env['F90']
        sys.exit(1)
    base = os.path.basename(F90)
    context.Message("checking %s type for cfortran.h ... " % base)
    cfortran = fortran.get(base,'NAGf90Fortran')
    context.env['CFORTRAN90'] = cfortran 
    context.Result(cfortran)
    context.Message("checking F90 module extension ... ")
    f90module = re.compile(r'(?:testf90|TESTF90)(\.\w+)$')
    suffix = ''
    for file in os.listdir(os.getcwd()):
        gotit = f90module.match(file)
        if gotit:
            suffix = gotit.group(1)
            os.remove(file)
            break
    context.env['F90MODSUFFIX'] = suffix
    context.Result(suffix)

def intel(context):
    '''Trying to fix wierd intel setup.'''
    libdirs = string.split(os.environ.get('LD_LIBRARY_PATH',''),':')
    libs = filter (lambda x: re.search('intel',x) and os.path.isdir(x),
                   libdirs)
    context.env.Append(ENV={'LD_LIBRARY_PATH':string.join(libs,':')})
    for key in ('INTEL_FLEXLM_LICENSE','INTEL_LICENSE_FILE','IA32ROOT'):
        license = os.environ.get(key) 
        if license:
            context.env.Append(ENV={key:license})

def options(opts):
    opts.Add('ENV','SCons environment')
    opts.Add('AR','Static library archiver')
    opts.Add('JPEG','The libjpeg library')
    opts.Add('PPM','The netpbm library')
    opts.Add('CC','The C compiler')
    opts.Add('CCFLAGS','General options that are passed to the C compiler',
             '-O2')
    opts.Add('CPPPATH',
             'The list of directories that the C preprocessor will search')
    opts.Add('LIBPATH',
             'The list of directories that will be searched for libraries')
    opts.Add('LIBS',
             'The list of libraries that will be linked with executables')
    opts.Add('XLIBPATH','Location of X11 libraries')
    opts.Add('XLIBS','X11 libraries')
    opts.Add('XINC','Location of X11 headers')
    opts.Add('PROGPREFIX','The prefix used for executable file names','sf')
    opts.Add('API','Support for additional languages (possible values: c++, fortran, fortran-90, python)')
    opts.Add('CXX','The C++ compiler')
    opts.Add('CXXFLAGS','General options that are passed to the C++ compiler',
             '-O2')
    opts.Add('F77','The Fortran-77 compiler')
    opts.Add('F77FLAGS','General options that are passed to the F77 compiler',
             '-O2')
    opts.Add('CFORTRAN','Type of the Fortran-77 compiler (for cfortran.h)')
    opts.Add('F90','The Fortran-90 compiler')
    opts.Add('F90FLAGS','General options that are passed to the F90 compiler',
             '-O2')
    opts.Add('CFORTRAN90','Type of the Fortran-90 compiler (for cfortran.h)')
    opts.Add('F90MODSUFFIX','Suffix of Fortran-90 module interface files')

local_include = re.compile(r'\s*\#include\s*\"([^\"]+)')

def includes(list,file):
    global local_include
    fd = open(file,'r')
    for line in fd.readlines():
         match = local_include.match(line)            
         if match:
             other = os.path.join(os.path.dirname(file),match.group(1))
             if not other in list:
                 includes(list,other)
    list.append(file)
    fd.close()

def merge(target=None,source=None,env=None):
    global local_include
    sources = map(str,source)
    incs = []
    for src in sources:
        if not src in incs:
            includes(incs,src)
    out = open(str(target[0]),'w')
    for src in incs:
        inp = open(src,'r')
        for line in inp.readlines():
            if not local_include.match(line):
                out.write(line)
        inp.close()
    out.close()
    return 0

docmerge = '''echo "import rsfdoc" > $TARGET
echo "" >> $TARGET
cat $SOURCES >> $TARGET'''

def docextra(docmerge,source,copy):
    return docmerge + '''
    echo rsfdoc.progs[\\'%s\\']=%s >> $TARGET''' % (copy,source)

#	$Id$
