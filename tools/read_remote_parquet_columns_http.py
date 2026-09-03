from __future__ import annotations
import io, time, requests
from collections import OrderedDict

class HTTPRangeReader(io.RawIOBase):
    def __init__(self,url:str,size:int,block_size:int=4*1024*1024,max_blocks:int=24):
        self.url=url; self.size=size; self.pos=0; self.block_size=block_size; self.max_blocks=max_blocks; self.cache=OrderedDict(); self.bytes_fetched=0; self.requests_count=0
    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self,offset,whence=io.SEEK_SET):
        if whence==io.SEEK_SET: p=offset
        elif whence==io.SEEK_CUR: p=self.pos+offset
        elif whence==io.SEEK_END: p=self.size+offset
        else: raise ValueError(whence)
        if p<0: raise ValueError('negative seek')
        self.pos=min(p,self.size); return self.pos
    def _get_block(self,bi:int)->bytes:
        if bi in self.cache:
            data=self.cache.pop(bi); self.cache[bi]=data; return data
        start=bi*self.block_size; end=min(self.size-1,start+self.block_size-1)
        last=None
        for attempt in range(1,7):
            try:
                r=requests.get(self.url,headers={'Range':f'bytes={start}-{end}','Accept-Encoding':'identity'},timeout=75)
                if r.status_code!=206: raise RuntimeError(f'status {r.status_code}')
                cr=r.headers.get('content-range',''); want=f'bytes {start}-{end}/{self.size}'
                if cr!=want: raise RuntimeError(f'content-range {cr!r} != {want!r}')
                data=r.content
                if len(data)!=(end-start+1): raise RuntimeError(f'length {len(data)} != {end-start+1}')
                self.bytes_fetched += len(data); self.requests_count += 1
                self.cache[bi]=data
                while len(self.cache)>self.max_blocks: self.cache.popitem(last=False)
                return data
            except Exception as e:
                last=e; time.sleep(min(12,attempt*2))
        raise RuntimeError(f'range fetch failed {start}-{end}: {last}')
    def read(self,n=-1):
        if self.pos>=self.size: return b''
        if n is None or n<0: n=self.size-self.pos
        n=min(n,self.size-self.pos); out=bytearray(); remaining=n
        while remaining:
            bi=self.pos//self.block_size; block=self._get_block(bi); off=self.pos-bi*self.block_size; take=min(remaining,len(block)-off)
            out.extend(block[off:off+take]); self.pos+=take; remaining-=take
        return bytes(out)
    def readinto(self,b):
        data=self.read(len(b)); b[:len(data)]=data; return len(data)
