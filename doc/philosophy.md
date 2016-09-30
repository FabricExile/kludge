# The Kludge Wrapping Philosophy

The approach that Kludge takes when wrapping C++ code is allow you to incrementally build up the wrapping of a C++ library.  Except in the particular case of members of in-place wrapped types (see [Wrapping Types](adl-types.md)), Kludge doesn't require you to wrap all of anything; you can only wrap as little or as much as you need.

There are several reasons for this approach:

- Kludge itself is expected to evolve over time.  There are things that Kludge can't do today but will be able to do tomorrow.  We want Kludge to be useful today, so we allow you to ignore the parts that Kludge simply can't wrap.

- There may be parts of a library that you don't want to expose in KL because they are confusing or unsafe.

## Using the results of `kludge discover`

As seen in the tutorials, `kludge discover` is a powerful tool for automatically writing an API description for C++ headers.  However, C++ is a tricky language, and there are cases where `kludge discover` will get it wrong.

Rather than simply fail in these cases, it is expected that the user will sometimes need to modify the results of `kludge discover` to fix these issues.  Except in the case of members of in-place types, it's always OK to comment out or erase parts of the `kludge discover` results that don't work.  Alternatively, you can fix them: the API description language is meant to be easily understood by both people and `kludge generate`.

## Kludge is Loose

To understand how Kludge works, one must step back and understand that Kludge doesn't actually do anything except generate KL and C++ code to wrap a C++ API.  As such, you don't always have to be exactly right when specifying the types of parameters and return values in Kludge; in many cases you can rely on C++'s automatic casting features to happen in the generated wrapping.

Next: [Wrapping Functions](adl-functions.md)
