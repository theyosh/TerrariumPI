---
title: FAQ
icon: fas fa-question
order: 10
layout: post

image:
  src: /assets/img/FAQ.webp
  width: 100%
  height: auto
  alt: FAQ header image
---
<style>
ul.jekyllcodex_accordion {padding-left: 0rem; position: relative; margin: 1.4rem 0!important; border-bottom: 1px solid rgba(0,0,0,0.25); padding-bottom: 0;}
ul.jekyllcodex_accordion > li {border-top: 1px solid rgba(0,0,0,0.25); list-style: none; margin-left: 0;}
ul.jekyllcodex_accordion li input {display: none;}
ul.jekyllcodex_accordion li label {display: block; cursor: pointer; padding: 0.75rem 2.4rem 0.75rem 0; margin: 0;}
ul.jekyllcodex_accordion li div {display: none; padding-bottom: 1.2rem;}
ul.jekyllcodex_accordion li input:checked + label {font-weight: bold;}
ul.jekyllcodex_accordion li input:checked + label + div {display: block;}
ul.jekyllcodex_accordion li label::before {content: "+"; font-weight: normal; font-size: 130%; line-height: 1.1rem; padding: 0; position: absolute; right: 0.5rem; transition: all 0.15s ease-in-out;}
ul.jekyllcodex_accordion li input:checked + label::before {transform: rotate(-45deg);}
i.far.fa-circle {display: none;}
</style>

Here you can find the most frequently asked question.

## Questions
{% assign faqs = site.faq | sort_natural: "title" %}
<ul class="jekyllcodex_accordion">
{% for faq in faqs %}
<li><input id="faq{{ forloop.index }}" type="checkbox" /><label for="faq{{ forloop.index }}">{{ faq.title }}</label><div>{{ faq.content | markdownify }}</div></li>
{% endfor %}
</ul>