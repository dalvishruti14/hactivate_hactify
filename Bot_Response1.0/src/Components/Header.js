import "../Styles/Header.css";

const Header = () => {
  const openStreamlitPage = () => {
    const streamlitURL = 'http://192.168.223.197:8501';
    
    // Open Streamlit page in a new tab or window
    window.open(streamlitURL, '_blank');
  };
  return (
    <div>
      <section id="logo">
    <nav class="navbar navbar-expand-lg " id="navbar-custom">
      <div class="container-fluid">
        {/* <a class="navbar-brand" href="#">
        <img src="robot.jpg" alt="Logo" width="100" height="70" class="d-inline-block align-text-top"/></a> */}
        <a class="navbar-brand " id="brand-text" href="/">SensoryLearn</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarText">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-auto">
            <li class="nav-item">
              <a class="nav-link active" id="home" aria-current="page" href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/products">Subjects</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/login" onClick={openStreamlitPage}>Ask Doubts</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

  </section>
    </div>
  )
}


export default Header