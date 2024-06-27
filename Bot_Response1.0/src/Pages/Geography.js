import React,{ useEffect, useState } from 'react';
import '../Styles/Geography.css';


function Geography() {

  const [answer, setAnswer] = useState("Loading");
  const [text, setText] = useState("Loading");
  useEffect(() => {
    fetch("/api/answer/")
    .then(res => res.json())
    .then(data => {
      setAnswer(data.answer);
      setText(data.answer.toString().replace(/\*/g, ''));
    });

    const handleBeforeUnload = () => {
      window.speechSynthesis.cancel();
    };

    // Add the 'beforeunload' event listener
    window.addEventListener('beforeunload', handleBeforeUnload);

    // Clean up function to remove the 'beforeunload' event listener
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      window.speechSynthesis.cancel();
    };
  }, []);

  useEffect(() => {
    // Cleanup speech synthesis when answer changes
    window.speechSynthesis.cancel();
  }, [answer]);

  const  Sound = () => {
    let utterance = new SpeechSynthesisUtterance();
    utterance.text = text;
    utterance.voice = window.speechSynthesis.getVoices()[0];
    window.speechSynthesis.speak(utterance);

  }

  const handleNextClick = () => {
    fetch("/api/next-word/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ word: 'Asia' }),
    })
      .then(res => res.json())
      .then(data => {
        setAnswer(data.answer);
        setText(data.answer.toString().replace(/\*/g, ''));
      })
  };
  
  return (

    <div>
    <div class="box-form">
<div class="left">
  <div class="overlay">
    <button type='submit' onClick={Sound}>Listen </button>
  </div>
</div>
  <div class="right">
  {answer}
</div>
</div>
<button type='submit' onClick={handleNextClick}>Next </button>
  </div>
    );
  
}

export default Geography;
