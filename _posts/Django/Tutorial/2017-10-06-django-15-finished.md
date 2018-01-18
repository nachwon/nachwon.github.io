---
layout: post
title: '[Django Tutorial] Blog 만들기 - 15. 마무리'
category: Django
tags:
  - Django
  - Tutorial
---



블로그에 추가적으로 잡다한 기능을 구현해주고 `CSS` 도 조금 손봐주었다.  
추가 사항은 아래와 같다.

- 글 게시하기 체크박스를 만들어 새 글을 등록할 때 체크하면 글을 메인 화면에 등록
- 새 글을 추가할 때 제목이나 내용이 비어있을 경우 글이 등록되지 않고 글 등록 페이지로 되돌아옴. 이 때, 제목이나 내용 중 작성되어있던 항목이 있을 경우 그 내용을 보존
- `html` 과 `CSS` 파일들을 수정하여 조금 꾸며주었음

배운것들을 응용해서 위의 기능을 구현해보자.

이 튜토리얼을 통해 최종 완성된 블로그의 코드는 [여기](https://github.com/nachwon/Djangogirls_assignment) 에서 확인할 수 있다.

- - -

지금까지 Python 웹프레임워크인 `Django` 를 활용하여 간단한 블로그를 한 번 만들어보았다. `Django` 를 이해하는데 도움이 되었길 바란다.

- - -

{% include tutorial-toc-base.html %}

- - -

