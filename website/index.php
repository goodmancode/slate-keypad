<!DOCTYPE html>
<html lang="en">
  <!-- Read in html head -->
  <?php readfile('./html/head.html'); ?>
  <body>
    <!-- Read in navbar element -->
    <?php readfile("./html/navbar.html"); ?>
    <div class="container">
      <div class="row mt-5 justify-content-center">
        <div class="col-lg-5 col-md-8 col-10">
          <img class="img-fluid" src="img/slate_showcaserender.png" alt="Slate PCB render"> 
        </div>
      </div>
      <div class="row mt-5">
        <h1 class="display-2 text-center">Slate</h1>
      </div>
      <div class="row">
        <h1 class="display-6 text-center">A multi-input programmable wireless macro keypad.</h1>
      </div>
      <div class="row mt-5 mx-2 justify-content-center">
        <div class="col-lg">
          <p class="text-center">“Slate” is a customizable, multi-input, wireless-capable macro keypad that combines a touchscreen display and multiple physical inputs, all in a compact and robust form factor. With the Slate configuration software, a user can intuitively apply desired shortcuts and keystrokes to one of 16 discrete physical inputs and up to 12 on-screen keys. These inputs then execute macros to a host device plugged in via USB, or wirelessly with its built-in battery and Bluetooth capability. Multiple selectable profiles allow the user to store and use macros for several applications. Macro capability includes typing a desired line of text, executing one or many keystrokes, media control, and more. It can be time-consuming for the user to memorize key-combinations for each program and across modern operating systems. With Slate, we aim to speed up common computer-based tasks for professionals, creators, and everyday users alike.</p>
          <hr/>
          <p class="text-center">Slate was created as part of the EE/CPE Senior Design program at UCF, and completed in the Fall 2021 semester.</p>
        </div>
      </div>
    </div>
    <!-- Read in required scripts -->
    <?php readfile('./html/scripts.html'); ?>
  </body>
</html>