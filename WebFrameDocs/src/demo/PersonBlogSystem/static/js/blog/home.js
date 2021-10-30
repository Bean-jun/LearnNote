$(function () {
    var $title = $('.title');
    $title.click(function () {
        fid = $(this).attr('fid');
        id = 'content_' + fid;
        $(this).next().show(1000, 'swing');
        previewMarkdown(id);
    });
// {#文本详细内容隐藏#}
    $('.panel-body').click(function () {
        $(this).hide(1000, 'swing');
    });
})

// 处理Markdown预览
function previewMarkdown(id) {
    editormd.markdownToHTML(id, {
// {#避免一些攻击#}
        htmlDecode: 'Style.script.iframe'
    });
}
