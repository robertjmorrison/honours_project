/**
 * Created by rjm on 20/03/2017.
 */

function showAnalysis() {
    $('#video-plays').addClass('hidden');
    $('#charts').removeClass('hidden');
    $('#breakdown-vids').removeClass('hidden');
    $('#quarters').addClass('hidden');
    $('#analysis-link').addClass('hidden');
    $('#video-link').removeClass('hidden');
    console.log("show analysis");
    chart.reflow();
}

function showVideo() {
    $('#video-plays').removeClass('hidden');
    $('#charts').addClass('hidden');
    $('#breakdown-vids').addClass('hidden');
    $('#quarters').removeClass('hidden');
    $('#analysis-link').removeClass('hidden');
    $('#video-link').addClass('hidden');
}

function chartGen() {

}

function yardsTrend() {

}

