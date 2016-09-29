# Tutorial: More About Using C++ Types

In the last tutorial we had to explicitly convery a KL array of integers into an STL vector in order to call a C++ function to reverse the elements of the vector.

An obvious question is, why doesn't Kludge just automatically convert the vector?  The answer lies in a key design aspect of Kludge: **Kludge will try to make the extension as easy to use as possible, but not at the cost of significant performance loss**.

In this case, if we were to implicitly convert KL vectors into STL vectors, there would be a hidden performance cost that users need to be aware of.  For a large vector (with hundreds of million of elements) the cost of converting the vector back and forth is significant and should be avoided.

So how does one avoid this conversion?  The answer is that Kludge allows you to use C++ types directly without ever using KL types for cases where this performance really matters.  This is illustrated with the following example that uses the `STLUser` extension we built in the last tutorial:

```
require STLUser;
operator entry() {
  SInt32_StdVector a;
  for (SInt32 i = 0; i < 10; ++i)
    a.push_back(i);
  report("a = " + a);
  report("ReverseVector(a) = " + ReverseVector(a));
}
```

Running this gives the output:

```
a = SInt32_StdVector:[0,1,2,3,4,5,6,7,8,9]
ReverseVector(a) = SInt32_StdVector:[9,8,7,6,5,4,3,2,1,0]
```

The result is the same, but we just created the STL vector directly rather than converting one from KL.  Notice that the STL vector was created using the `push_back` method rather than the KL equivalent `push` method; this is because this is how the method is named in C++.
