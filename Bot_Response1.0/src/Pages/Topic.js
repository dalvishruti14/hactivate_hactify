import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { useNavigate, useLocation } from 'react-router-dom';
import Header from './HeadG';
import Footer from './FootG';
import { getFirestore, collection, setDoc, addDoc, doc, getDoc } from 'firebase/firestore';

function Topic() {
  const [answer, setAnswer] = useState("Loading");
  const [audioFilePath, setAudioFilePath] = useState("");
  const [isMounted, setIsMounted] = useState(false);
  let audioPlayer = null;
  const navigate = useNavigate();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const param1 = params.get("param1");
  const param2 = params.get("param2");
  const param3 = params.get("param3");
  let param4 = params.get("param4");

  const db = getFirestore();

  const saveData = async () => {
    if (answer !== "Loading") {
      const docRef = doc(db, "answers", `${param1}_${param2}_${param3}_${param4}`);
      
      try {
        // Create or update the document with the specified document ID
        await setDoc(docRef, {
          answer: answer,
        });
        console.log('Data saved to Firestore');
        console.log("Saved document:", docRef.id);
      } catch (error) {
        console.error('Error saving data to Firestore:', error);
      }
    }
  };

  console.log("Params:", param1, param2, param3, param4);

  useEffect(() => {
    // Set isMounted to true when the component mounts
    setIsMounted(true);

    // Cleanup function to set isMounted to false when the component unmounts
    return () => {
      setIsMounted(false);
    };
  }, []);

  useEffect(() => {
    // Call checkFirestoreEntry only when the component is mounted
    if (isMounted) {
      checkFirestoreEntry();
    }

    const handleBeforeUnload = () => {
      stopAudio();
    };

    // Add the 'beforeunload' event listener
    window.addEventListener('beforeunload', handleBeforeUnload);

    // Clean up function to remove the 'beforeunload' event listener
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      stopAudio();
    };
  }, [param1, param2, param3, param4, isMounted]); // Dependencies are set to params and isMounted

 const checkFirestoreEntry = async () => {
  const docRef = doc(db, "answers", `${param1}_${param2}_${param3}_${param4}`);
  console.log("Checking Firestore entry:", docRef);
  
  try {
    const docSnap = await getDoc(docRef);
    console.log("Document data:", docSnap.data());
    
    if (docSnap.exists()) {
      console.log("Document exists!");
      const data = docSnap.data();
      fetch("/api/listen/", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: data.answer, language: param2}),
      })
        .then(res => res.json())
        .then(data => {
          console.log('Fetched audio:', data);
          setAudioFilePath(data.audio_file_path);
        })
        .catch(error => {
          console.error('Error fetching audio:', error);
        });
      setAnswer(data.answer);
      setAudioFilePath(data.audioFilePath);
      stopAudio();
    } else {
      console.log("No such document!");
      fetchData();
    }
  } catch (error) {
    console.error('Error checking document existence:', error);
  }
};


  const fetchData = () => {
    // Use these values in the fetch request
    fetch("/api/answer/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ age: param1, language: param2, subject: param3, number: param4 }),
    })
      .then(res => res.json())
      .then(data => {
        setAnswer(data.answer);
        console.log('Fetched data:', answer);
        setAudioFilePath(data.audio_file_path);
        stopAudio();
        
        console.log('Data saved to Firestore');
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };

  useEffect(() => {
    // Call saveData only when the answer state changes
    saveData();
  }, [answer]);
  
  const handleNextButtonClick = () => {
    navigate(`/topic?param1=${param1}&param2=${param2}&param3=${param3}&param4=${parseInt(param4) + 1}`);
  };

  const playAudio = () => {
    if (audioFilePath) {
      const timestamp = new Date().getTime();
      const audioUrl = `http://localhost:5000/api/get-audio/?timestamp=${timestamp}`;
      audioPlayer = new Audio(audioUrl);
      audioPlayer.play();
      console.log('Playing audio:', audioFilePath);
    }
  };

  const stopAudio = () => {
    if (audioPlayer) {
      audioPlayer.pause();
      audioPlayer.currentTime = 0;
      console.log('Audio stopped');
    }
  };

  const Wrapper = styled.div`
    //margin-top: 50px; /* Adjust as needed for header space */
    //margin-bottom: 50px; /* Adjust as needed for footer space */
  `;

  const BoxForm = styled.div`
    margin-top: 50px;
    margin-left: 50px;
    margin-bottom: 100px;
    margin-right: 50px;
    width: 92%;
    height: 100%;
    background: #f3c8c8;
    border-radius: 10px;
    overflow: hidden;
    display: flex;
    flex: 1 1 100%;
    align-items: stretch;
    justify-content: space-between;
    box-shadow: 0 0 20px 6px #dc6d6d85;
  `;

  const Left = styled.div`
    .overlay {
      padding: 30px;
      margin-top: 4rem;
      width: 100%;
      height: 100%;
      overflow: hidden;
      box-sizing: border-box;
    }

    button {
      margin : 10px;
      float: auto;
      text-align: center;
      width:150px;
      text-align:center;
      margin-left:auto;
      color: #000000;
      font-size: 16px;
      padding: 12px 35px;
      border-radius: 50px;
      display: inline-block;
      border: 0;
      outline: 0;
      box-shadow: 0px 4px 20px 0px #666f78a6;
      background-image: linear-gradient(135deg, #e1515196 10%, #ff5151 100%);
    }
  `;

  const Right = styled.div`
    padding: 40px;
    overflow: hidden;
  `;

  const NextButton = styled.button`
    float: right;
    color: #000000;
    font-size: 16px;
    padding: 12px 35px;
    border-radius: 50px;
    display: inline -block;
    border: 0;
    outline: 0;
    box-shadow: 0px 4px 20px 0px #666f78a6;
    background-image: linear-gradient(135deg, #e1515196 10%, #ff5151 100%);
    margin-top: -70px;
  `;

  return (
    <>
      <Header />
      <Wrapper>
        <BoxForm className="box-form">
          <Left className="left">
            <div className="overlay">
              <button type='submit' onClick={playAudio}>Listen </button>
              <button type='submit' onClick={stopAudio}>Stop </button>
              <button type='submit'>Sign Language </button>
            </div>
          </Left>
          <Right className="right">
            {answer}
          </Right>
        </BoxForm>
        <NextButton type='submit' onClick={handleNextButtonClick}>Next </NextButton>
      </Wrapper>
      <Footer />
    </>
  );
}

export default Topic;
