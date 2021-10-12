---
title: FAQ
icon: fas fa-question
order: 10

image:
  src: /assets/img/FAQ.webp
  alt: "FAQ header image"
---
Here you can find the most frequently asked question.

{% assign faqs = site.faq | sort_natural: "title" %}
<ul class="jekyllcodex_accordion">
{% for faq in faqs %}
  <li>
    <input id="faq{{ forloop.index }}" type="checkbox" />
    <label for="faq{{ forloop.index }}"><h2>{{ faq.title }}</h2></label>
    <div class="faq_content">{{ faq.content | liquify | markdownify }}</div>
  </li>
{% endfor %}
</ul>
<script>
jQuery(document).ready(function() {
  setTimeout(function(){
    let faq = $(location).attr('hash').slice(1);
    console.log('FAQ',faq);
    if ('' != faq) {
      jQuery('#' + faq).parent().click();
    }
  },700)
})
</script>