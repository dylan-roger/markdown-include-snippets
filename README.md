# Markdown-Include-Snippets

Based on project https://github.com/cmacmackin/markdown-include

## Installation

```sh
pip install git+https://github.com/fonimus/markdown-include-snippets.git
```

## Usage

* Include file, just like **markdown-include**

  ```sh
  {!filename!}
  ```
  
* Include file snippet with tag

  ```sh
  {!filename!tag=tagname}
  ```
  
  Source filename:
  
  ```java
  package io.fonimus;

  public class Test {

      // tag::tagname
      public void test(){

      }
      // end::tagname

  }
  ```
  
  
## Notes

* If tag is not found, all file is included
* If start tag or end tag is not found, all file is included
* If file is not found, blank line is added
