title:	DictField parsing for "html" inputs misleadingly returns an empty dict even if the field was not specified
state:	OPEN
author:	brett-lempereur (Brett Lempereur)
labels:	
comments:	3
assignees:	
projects:	
milestone:	
number:	6234
--
## Checklist

- [x] I have verified that that issue exists against the `master` branch of Django REST framework.
- [x] I have searched for similar issues in both open and closed tickets and cannot find a duplicate.
- [x] This is not a usage question. (Those should be directed to the [discussion group](https://groups.google.com/forum/#!forum/django-rest-framework) instead.)
- [x] This cannot be dealt with as a third party library. (We prefer new functionality to be [in the form of third party libraries](https://www.django-rest-framework.org/topics/third-party-resources/#about-third-party-packages) where possible.)
- [x] I have reduced the issue to the simplest possible case.
- [ ] I have included a failing test as a pull request. (If you are unable to do so we can still accept the issue.)

## Steps to reproduce

Using a DictField and custom partial update logic in a serializer, a condition such as:

`if not self.partial or "field-name" in data:`

Is always true when the request type is `multipart/form-data`, even if the field was not specified.  In fact, in this case, it seems like it is impossible to distinguish between an empty input and an unspecified input for that field.

## Expected behavior

The condition `if not self.partial or "field-name" in data` should only be true when the field was specified by the client, even when using `multipart/form-data` requests.

## Actual behavior

The condition is always true for `mutlipart/form-data` requests, even when the field was not specified as part of the request, and the update method has no way to distinguish between an empty input and an unspecified field.

Note that this is not the case for ListField, and the problem seems to be in the return of the function at https://github.com/encode/django-rest-framework/blob/master/rest_framework/utils/html.py#L69.  The equivalent function for a list field returns an empty value if no matching elements were found in the input.  For the dict field parsing logic, an empty dictionary is incorrectly returned.
