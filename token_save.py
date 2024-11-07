
# 00시 05분(크론탭) 토큰 생성


import KIS_Common as Common

Common.MakeToken(dist="VIRTUAL")
print("REAL TOKEN:" , Common.GetToken("REAL"))
print("VIRTUAL TOKEN:" , Common.GetToken("VIRTUAL"))