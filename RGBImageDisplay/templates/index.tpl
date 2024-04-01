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
      {% for _, image_group in image_groups.items()|sort %}
        <li>
          <code>{{ image_group.name }}</code> ({{ image_group.images | length }}):
          <ul>
            {% for _, image_info in image_group.images.items()|sort %}
              <li>
                <button class="play"
                  data-group="{{ image_group.name }}"
                  data-image="{{ image_info.name }}">
                  Play
                </button>
                <code>{{ image_info.name }}</code>
              </li>
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
    <span id="frame_parent">?</span>:<span id="frame_name">?</span>,
    <span id="frame_index">?</span>/<span id="frame_count">?</span>
  </span>

  <br/>

  <span class="right_panel border">
    <img src="/stream" style="width: {{ width * 7 }}px; height: {{ height * 7 }}px;" />
  </span>
{% endblock %}
