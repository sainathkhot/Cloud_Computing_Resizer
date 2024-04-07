import React from "react";
import "../components/Aboutuscontent.css";
import yashprofile from '../assets/yash.jpeg';


const Aboutuscontent = () => {
  return (
    <div className="team-members-container">
    <div className="member-card">
      <img src={yashprofile} alt="Member 1" className="member-photo" />
      <h2>Yash Malekar</h2>
      <p>Role: Pookie</p>
    </div>
    <div className="member-card">
      <img src={yashprofile} alt="Member 2" className="member-photo" />
      <h2>Amba Singh</h2>
      <p>Role: Bussinnnn</p>
    </div>
    <div className="member-card">
      <img src={yashprofile} alt="Member 3" className="member-photo" />
      <h2>Osama</h2>
      <p>Role: H.O.D</p>
    </div>
  </div>
  )
}

export default Aboutuscontent
