# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import libc
from ctypes import *
import cv2

libc.StrToPtr.argtypes=[c_char_p]
libc.StrToPtr.restype=c_void_p
def _StrToPtr(worldstr):
    worldbytes=worldstr.encode('utf-8')
    cptr=c_char_p(worldbytes)
    voidptr=libc.StrToPtr(cptr)
    return voidptr

libc.GetCurrentLevel.argtypes=[c_void_p]
libc.GetCurrentLevel.restype=c_void_p
def GetCurrentLevel(uworld):
    return libc.GetCurrentLevel(uworld)

#libc.GetNumberOfLevelBluePrints.argtypes=[c_void_p]
#libc.GetNumberOfLevelBluePrints.restype=c_int
#def GetNumberOfLevelBluePrints(ulevel):
#    return libc.GetNumberOfLevelBluePrints(ulevel)

libc.GetActorCount.argtypes=[c_void_p]
libc.GetActorCount.restype=c_int
def GetActorCount(uworld):
    return libc.GetActorCount(uworld)

libc.FindActorByName.argtypes=[c_void_p,c_char_p,c_int]
libc.FindActorByName.restype=c_void_p
def FindActorByName(uworld,name,verbose=0):
    namebytes=name.encode('utf-8')
    #namebytes=name.encode('utf-16-le')
    return libc.FindActorByName(uworld,namebytes,verbose)

libc.GetActorsNames.argtypes=[c_void_p,c_void_p,c_int]
libc.GetActorsNames.restype=c_int
def GetActorsNames(uworld,bufsize=1024*10):
    buf=b'\0'*bufsize
    sz=sizeof(c_wchar)
    ret=libc.GetActorsNames(uworld,buf,int(bufsize/sz))
    if ret==-1: 
        print('Error in GetActorsNames try bigger buf size')
        return None
    names=buf[:ret*sz].decode('utf16').strip().split('\n')
    return names

float3type=c_float*3
float3type_p=POINTER(float3type)
libc.GetActorLocation.argtypes=[c_void_p,float3type_p]
def GetActorLocation(actor):
    vec=float3type()
    libc.GetActorLocation(actor,pointer(vec))
    return tuple(vec)

libc.SetActorLocation.argtypes=[c_void_p,float3type_p]
def SetActorLocation(actor,invec):
    vec=float3type(*invec)
    libc.SetActorLocation(actor,vec)

libc.GetActorRotation.argtypes=[c_void_p,float3type_p]
def GetActorRotation(actor):
    vec=float3type()
    libc.GetActorRotation(actor,pointer(vec))
    return tuple(vec)

libc.SetActorRotation.argtypes=[c_void_p,float3type_p]
def SetActorRotation(actor,invec):
    vec=float3type(*invec)
    libc.SetActorRotation(actor,vec)



libc.MoveToCameraActor.argtypes=[c_void_p,c_void_p,c_int]
def MoveToCameraActor(actor,camera,index=0):
    libc.MoveToCameraActor(actor,camera,index)

int2type=c_int*2
libc.GetViewPortSize.argtypes=[POINTER(int2type)]
libc.TakeScreenshot.argtypes=[c_void_p,c_int]
import cv2
import numpy as np
tmp_capture_mem=np.array([1],dtype='uint8')


libc.GetTextureByName.argtypes=[c_char_p,c_int]
libc.GetTextureByName.restype=c_void_p
def GetTextureByName(name):
    nm=name.encode('utf-16-le')
    print('[=={}==]'.format(name),len(nm))
    return libc.GetTextureByName(nm,1)



libc.GetTextureData.argtypes=[c_void_p,c_void_p,c_int]
libc.GetTextureData.restype=c_int
libc.GetTextureSize2.argtypes=[c_void_p,POINTER(int2type)]
libc.GetTextureSize2.restype=c_int
def GetTextureData(tex_ptr,channels=[0,1,2]):
    global tmp_capture_mem
    sz=int2type()
    ret=libc.GetTextureSize2(tex_ptr,pointer(sz))
    req_mem_sz=sz[0]*sz[1]*4# (RGBA)
    if len(tmp_capture_mem)<req_mem_sz:
        tmp_capture_mem=np.zeros(req_mem_sz,'uint8')
    ptr=tmp_capture_mem.ctypes.data_as(c_void_p)
    libc.GetTextureData(tex_ptr,ptr,req_mem_sz)
    return tmp_capture_mem[:req_mem_sz].reshape((sz[1],sz[0],4))[:,:,channels]

if 1:
    libc.GetTextureDataf.argtypes=[c_void_p,c_void_p,c_int,c_int]
    libc.GetTextureDataf.restype=c_int

    tmp_capture_memf=np.array([1],'float16')

    def GetTextureData16f(tex_ptr,channels=[0,1,2],verbose=0):
        global tmp_capture_memf
        sz=int2type()
        ret=libc.GetTextureSize2(tex_ptr,pointer(sz))
        req_mem_sz=sz[0]*sz[1]*4# (RGBA)
        if len(tmp_capture_memf)<req_mem_sz:
            tmp_capture_memf=np.zeros(req_mem_sz,'float16')
        ptr=tmp_capture_memf.ctypes.data_as(c_void_p)
        if libc.GetTextureDataf(tex_ptr,ptr,req_mem_sz*2,verbose)==0:
            return None
        if verbose:
            stats_data=tmp_capture_memf[tmp_capture_memf!=65504.0]
            print('GetTextureData16f stats maxmin',stats_data.max(),stats_data.min())
        return tmp_capture_memf[:req_mem_sz].reshape((sz[1],sz[0],4))[:,:,channels]




#libc.GetTextureData.argtypes=[c_void_p,
#def GetTextureData


def TakeScreenshot():
        global tmp_capture_mem
        sz=int2type()
        libc.GetViewPortSize(pointer(sz))
        req_mem_sz=sz[0]*sz[1]*4# (RGBA)
        if len(tmp_capture_mem)<req_mem_sz:
            #tmp_capture_mem=b'\0'*req_mem_sz
            tmp_capture_mem=np.zeros(req_mem_sz,'uint8')
        ptr=tmp_capture_mem.ctypes.data_as(c_void_p)
        lsize=libc.TakeScreenshot(ptr,len(tmp_capture_mem))
        return tmp_capture_mem.reshape((sz[1],sz[0],4))[:,:,:3]

libc.SetWindParams.argtypes=[c_void_p,c_float,c_float]

#BUG!! does not work
def SetWindParams(awind,speed):
    libc.SetWindParams(awind,speed,speed)

libc.DeactivateActorComponent.argtypes=[c_void_p]
def DeactivateActor(actor):
    libc.DeactivateActorComponent(actor)


libc.ActivateActorComponent.argtypes=[c_void_p,c_bool]
def ActivateActor(actor):
    libc.ActivateActorComponent(actor,False)


libc.GetTextureSize.argtypes=[POINTER(int2type),c_int,c_bool]
libc.GetTexture.argtypes=[c_void_p,c_int,c_int,c_bool]
def GetTextureImg(txt_index=0,verbose=0,channels=[0,1,2]):
        global tmp_capture_mem
        sz=int2type()
        ret=libc.GetTextureSize(pointer(sz),txt_index,verbose)
        req_mem_sz=sz[0]*sz[1]*4# (RGBA)

        if len(tmp_capture_mem)<req_mem_sz:
            tmp_capture_mem=np.zeros(req_mem_sz,'uint8')
        ptr=tmp_capture_mem.ctypes.data_as(c_void_p)
        libc.GetTexture(ptr,req_mem_sz,txt_index,0)
        return tmp_capture_mem[:req_mem_sz].reshape((sz[1],sz[0],4))[:,:,channels]

libc.GetSceneCapture2DFrustrum.argtypes=[c_void_p,POINTER(c_float),POINTER(c_float)]
def GetSceneCapture2DNearFar(actor):
    near=c_float(-1)
    far=c_float(-1)
    libc.GetSceneCapture2DFrustrum(actor,pointer(near),pointer(far))
    return near.value,far.value
