import "../components/resizecontent.css";
import { useState } from 'react'
import React from 'react';


const Resizecontent = () => {

    const [file ,setfile] = useState(null);
    const [percentage ,setper] = useState(0);
    const [upscale, setup] = useState(false);
    const [downscale, setdown] = useState(false);
    console.log("UPSCALE : ",upscale);
  
    
  
    const Upscale = () => {
      setup(!upscale);
      setdown(false);
    }
  
    const Downscale = () => {
      setup(false);
      setdown(!downscale);
    }
  

    const resize = () => {
      console.log("FILE : ", file,
        "\nUP : ", upscale,
        "\nDown : ", downscale,
        "\nPer : ", percentage
      );
    }

  return (
    <div>
     <div className="resizecard" >
     <div className="showfile">
     {file && (
    <div>
        {file.type.startsWith('image') ? (
            // If the file is an image, display it
            <img src={URL.createObjectURL(file)} alt="Preview" style={{ maxWidth: '550px' ,maxHeight: '450px'}} />
        ) : (
            // If the file is a video, display it
            <video key={file.name} controls style={{ maxWidth:'550px' , maxHeight:'480px' }}>
                <source src={URL.createObjectURL(file)} type={file.type} />
                Your browser does not support the video tag.
            </video>
        )}
    </div>
)}  
</div>

      <div className="input">
        <div className="fileinput">
          Enter Your File
          <br />
          <input className='fileinputbox' type="file" accept="image/video/*" alt='' onChange={(e) => {setfile(e.target.files[0])}}></input>
        </div>
        
        <div className="scallingtoggle">
          UpScale or DownScale your file.
            <br/>
            <p >UpScale to expand & DownScale to compress your file </p>
          <div className='scallingswitchbox'>
          <div className="upscale">
            UpScale
          <label class="switch" >
            <input type="checkbox" checked={upscale} onChange={Upscale}/>
            <span class="slider round"></span>
          </label>
          </div>          
          <div className="downscale">
            DownScale
          <label class="switch">
            <input type="checkbox" checked={downscale} onChange={Downscale}/>
            <span class="slider round"></span>
          </label>
          </div>
        </div>
        </div>


        <div className="percentageinput">
          Percentage ( 1 ~ 100% )
          <br />
          <input className='percentageinputbox' type="number" min={1} max={100} onChange={ (e) => {setper(e.target.value)}}></input>
        </div>
        
        <button className="resize" onClick={resize}>Resize</button>

      </div>
    </div>
    </div>
  );
};

export default Resizecontent;