#!/bin/sh
# install script for MCSControl libraries and C header files
#
# usage:
# install_mcs.sh [-c] [arch] [path]
# -c:   library versions found under the installation base directory
#       are uninstalled
# arch: the target architecture (optional). If no arch option is
#       given, the systems architecture is used.
# path: the base directory for installing, e.g. /usr or /opt. 
#       defaults to /usr if omitted.

showhelp()
{
  printf "Usage: $(basename $0) [-c] [arch] [path]\n \
-c\tuninstall existing libraries\n \
arch\t(optional) the target architecture: -x86 or -x86_64.\n \
\tthe system architecture is used if omitted\n \
path\t(optional) the base directory for installing, e.g. /usr or /opt.\n \
\tdefaults to /usr if omitted.\n " \
>&2
}


uninstall()
{
  echo "uninstalling..."
  rm -f "$IPATH"/lib/libsmaractio*
  rm -f "$IPATH"/lib/libmcscontrol*
  rm -f "$IPATH"/lib/libftd2xx*
  rm -f "$IPATH"/lib/libftchipid*
  rm -f "$IPATH"/include/MCSControl.h
}


install()
{
  echo "installing $ARCH bit libraries to $IPATH"
  
  if [ ! -d "$IPATH/lib" ]; then
    mkdir -p "$IPATH/lib"
  fi
  if [ ! -d "$IPATH/include" ]; then
    mkdir -p "$IPATH/include"
  fi
  cp -a -f "$SRCPATH/include"/*.h "$IPATH/include/"

  cp -a -f "$SRCPATH/$ARCH/lib"/libmcscontrol.so* "$IPATH/lib/"
  cp -a -f "$SRCPATH/$ARCH/lib"/libsmaractio.so* "$IPATH/lib/"
  cp -a -f "$SRCPATH/$ARCH/lib"/libftd2xx.so* "$IPATH/lib/"
  cp -a -f "$SRCPATH/$ARCH/lib"/libftchipid.so* "$IPATH/lib/"
  ldconfig -n "$IPATH/lib"

  cd $OLDP
}


get_arch()
{
    local A=$(uname -m)
    if [ "$A" = "x86_64" ]; then 
        echo "arch_x86_64"
    elif [ "$A" = "i386" ] || [ "$A" = "i686" ]; then 
        echo "arch_x86"
    fi
    # else: empty
}


self="${0#./}"
base="${self%/*}"

SRCPATH=""
if [ "$base" = "$self" ]; then
    SRCPATH="$(pwd)"
else
    SRCPATH="$(pwd)/$base"
fi ;


DOUNINSTALL=""
IPATH="/usr"

if [ "$1" = "-h" ]; then
  showhelp;
  exit 2
fi

if [ "$1" = "-c" ]; then
  DOUNINSTALL=1;
  shift 1
fi

# may be empty if trying to install on non-x86 architecture
SYS_ARCH=$(get_arch)

ARCH=$SYS_ARCH
if [ "$1" = "-x86_64" ]; then
  ARCH=arch_x86_64
  shift 1
elif [ "$1" = "-x86" ]; then
  ARCH=arch_x86
  shift 1
fi

if [ "$ARCH" = "" ]; then
  echo "unknown or unsupported architecture. cannot install."
  return 1
fi

if [ -n "$1" ]; then
  IPATH=$1
fi

if [ ! -d "$IPATH" ]; then
  echo "installation path does not exist: $IPATH"
  return 1
fi

if [ -n "$DOUNINSTALL" ]; then
  uninstall;
else
  install;
fi
