{% extends 'base.tpl' %}

{% block title %}RGB Image Display Server{% endblock %}

{% block extra_head %}
  <link media="all" rel="stylesheet" href="/static/index.css" />
  <script src="/static/index.js"></script>
{% endblock %}

{% block content %}
  <span class="left_panel">
    Image Groups:
    <ul>
      {% for group_name, images in image_groups.items() %}
        <li>
          <code>{{ group_name }}</code> ({{ images | length }}):
          <ul>
            {% for image_name, image in images %}
              <li><code>{{ image_name }}</code></li>
            {% endfor %}
          </ul>
        </li>
      {% endfor %}
    </ul>
  </span>

  <span>
    {{ width }}x{{ height }}, {{ rotate * 90 }}°, {{ (alpha / 2.55) | int }}%, {{ (delay_seconds * 1000) | int }}ms
  </span>
  <span class="frame_info">
    ?
  </span>
  <br/>

  <span class="right_panel">
    <img src="/stream" style="width: {{ width * 7 }}px; height: {{ height * 7 }}px;" />
  </span>
{% endblock %}
