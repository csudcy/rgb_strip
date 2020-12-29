{% extends 'base.tpl' %}

{% block title %}RGB Image Display Server{% endblock %}

{% block extra_head %}
  <link media="all" rel="stylesheet" href="/static/index.css" />
  <script src="/static/index.js"></script>
{% endblock %}

{% block content %}
  <span class="left_panel border">
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

  <span class="border">
    {{ width }}x{{ height }},
    {{ rotate * 90 }}°,
    {{ (alpha / 2.55) | int }}%,
    {{ (delay_seconds * 1000) | int }}ms
    <button id="move_next">Next</button>
    <span id="frame_name">?</span>,
    <span id="frame_index">?</span>/<span id="frame_count">?</span>
  </span>

  <br/>

  <span class="right_panel border">
    <img src="/stream" style="width: {{ width * 7 }}px; height: {{ height * 7 }}px;" />
  </span>
{% endblock %}
