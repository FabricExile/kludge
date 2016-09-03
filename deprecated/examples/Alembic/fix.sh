fix()
{
  sed -i "s/::btAlignedObjectArray< $1 /::btAlignedObjectArray< ::$1 /" NewAlembic.cpp
}

#sed -i "s/::PODTraits< k/::Alembic::Util::v7::PODTraits< ::Alembic::Util::v7::k/" NewAlembic.cpp
#sed -i "s/, string/, std::string/" NewAlembic.cpp
#sed -i "s/, wstring/, std::wstring/" NewAlembic.cpp
sed -i "s/::limits< /::Imath_2_2::limits< /" NewAlembic.cpp
