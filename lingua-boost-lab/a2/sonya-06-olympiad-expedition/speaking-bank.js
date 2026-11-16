"use strict";
(()=>{const select=document.getElementById('bank-time'),out=document.getElementById('bank-clock'),start=document.getElementById('bank-start');let left=120,clock=null;
function draw(){out.textContent=String(Math.floor(left/60)).padStart(2,'0')+':'+String(left%60).padStart(2,'0');}
function pause(){clearInterval(clock);clock=null;start.textContent='Start / pause';}
function reset(){pause();left=Number(select.value);draw();}
select.addEventListener('change',reset);document.getElementById('bank-reset').onclick=reset;
start.onclick=()=>{if(clock){pause();return;}if(left<=0)left=Number(select.value);start.textContent='Pause';clock=setInterval(()=>{left--;draw();if(left<=0){pause();out.textContent='Time to reflect';}},1000);};
document.getElementById('bank-export').onclick=()=>window.OLYMPIAD_APP.exportWork();
})();
