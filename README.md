# Markdown Include Snippets

Based on project https://github.com/cmacmackin/markdown-include

## Installation

```sh
# release
pip install git+https://github.com/fonimus/markdown-include-snippets.git@<tag>
# master
pip install git+https://github.com/fonimus/markdown-include-snippets.git
```

## Usage
  
### Whole file inclusion

```java
{!/path/to/file.java!}
```

```java
package io.fonimus;

public class Test {

    // tag::test
    public void test(){

    }
    // end::test

}
```

### Tag snippet

```java
{!/path/to/file.java!tag=test}
```

```java
    public void test(){

    }
```

### Single line snippet

```java
{!/path/to/file.java!lines=3}
```

```java
public class Test {
```

### Line enumeration snippet

```java
{!/path/to/file.java!lines=1,3,6}
```

```java
package io.fonimus;
public class Test {
    public void test(){
```

### Line range snippet

```java
{!/path/to/file.java!lines=6-8}
```

```java
    public void test(){

    }
```
  
  
## Notes

* If file is not found, blank line is added
* If tag is not found, all file is included
* If start tag or end tag is not found, all file is included

