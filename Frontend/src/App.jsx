// import { useState } from "react";
// import axios from "axios";
// import "./App.css";
// import Loader from "./components/loader/loader.jsx";

// function App() {
//   // new line start
//   const [profileData, setProfileData] = useState(null);

//   //end of new line

//   return (
//     <div className="App">
//       <Loader>Loading...</Loader>
//     </div>
//   );
// }

// export default App;



import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./components/header/header.jsx";
import Login from "./components/Login.jsx";
import Register from "./components/Register.jsx";

function App() {
  return (
    <BrowserRouter>
      <Header />
      <div className="App">
        <Routes>
          <Route path="/" element={<h1>Welcome to LearnX 🚀</h1>} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;


