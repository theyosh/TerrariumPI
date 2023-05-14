---
title: FAQ
icon: fas fa-question
order: 11

image:
  path: /assets/img/FAQ.webp
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
jQuery(function() {
  setTimeout(function(){
    let faq = jQuery(location).attr('hash').slice(1);
    if ('' != faq) {
      jQuery('#' + faq).parent().click();
    }
  },500);
})
</script>
