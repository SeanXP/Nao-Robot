#!/bin/bash
#################################################################
#   Copyright (C) 2015 Sean Guo. All rights reserved.
#														  
#	> File Name:        < mv_to_nao.sh >
#	> Author:           < Sean Guo >		
#	> Mail:             < iseanxp+code@gmail.com >		
#	> Created Time:     < 2015/04/17 >
#	> Last Changed: 
#	> Description:
#################################################################

# 拷贝当前目录至Nao机器人系统中;
scp -r ../xpserver/ nao@192.168.2.100:~/.
