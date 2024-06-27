import React, { Component } from "react";
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Link,
} from "react-router-dom";

import Geography from "./Pages/Geography";
import Home from "./Pages/Home";
import Header from "./Components/Header";

const App = () => {
  return (
    <Router>
    <div className="App">
    {<Header />}
    <Routes>
    <Route exact path="/" element={<Home />}> </Route>
    <Route exact path="/geography" element={<Geography />}> </Route>
    </Routes>
    </div>
    </Router>
  );
};

export default App;
