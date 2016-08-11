sed -i 's/^_KLUDGE_LIB_errMsg$/\&_KLUDGE_LIB_errMsg/' USD.cpp
sed -i 's/^            _KLUDGE_LIB_result/            \&_KLUDGE_LIB_result/' USD.cpp
sed -i 's/^            _KLUDGE_LIB_whyNot/            \&_KLUDGE_LIB_whyNot/' USD.cpp
cat Conversions.cpp >>USD.cpp
