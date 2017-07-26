struct MyVec
{
  double x;
  double y;
};

class Class
{
public:

  Class(double x, double y)
  {
    m_v.x = x;
    m_v.y = y;
  }

  double x() const { return m_v.x; }
  double y() const { return m_v.y; }

  operator double*() { return (double*)&m_v; }
  operator const double*() const { return (const double*)&m_v; }
  operator MyVec&() { return m_v; }

private:
  MyVec m_v;
};

