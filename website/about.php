<!DOCTYPE html>
<html lang="en">
  <!-- Read in html head -->
  <?php readfile('./html/head.html'); ?>
  <body>
    <!-- Read in navbar element -->
    <?php readfile("./html/navbar.html"); ?>
    <div class="container mt-5">
      <h1>The Slate Team</h1>
      <hr/>
      <div class="row">
        <div class="col-lg">
          <img src="img/profile_diego.jpg" class="rounded mx-auto d-block my-4" style="width:96px;height:132px">
          <h3 class="text-center">Diego Agudelo</h3>
          <h5 class="text-muted text-center">BSCE</h5>
          <p class="text-center">Diego Agudelo is a senior design student expecting his BSCE form the University of Central Florida in December 2021. After graduation he will be pursuing a career in computer hardware in an undecided company. As with that he will be further expanding and growing his custom automotive lighting business. He plans to obtain his MSCpE after working and finishing his ongoing projects.</p>
        </div>
        <div class="col-lg">
          <img src="img/profile_andrew.jpg" class="rounded mx-auto d-block my-4" style="width:96px;height:132px">
          <h3 class="text-center">Andhres Bolano-Melendez</h3>
          <h5 class="text-muted text-center">BSCE</h5>
          <p class="text-center">Andhres Bolano-Melendez is a senior design student expecting his BSCE from the University of Central Florida in December 2021. After graduation he is pursuing a career as a Java/Python developer at IBM and possibly coming back to UCF to pursue a MSCpE.</p>
        </div>
        <div class="col-lg">
          <img src="img/profile_sam.jpg" class="rounded mx-auto d-block my-4" style="width:96px;height:132px">
          <h3 class="text-center">Samuel Chodur</h3>
          <h5 class="text-muted text-center">BSEE</h5>
          <p class="text-center">Samuel J. Chodur, Jr. is a senior student expecting his BSEE from the University of Central Florida in December 2021. He presently works for Leidos, Inc. as a Data Analyst supporting the United States Prompt Diagnostic System and the United States National Data Center at the Air Force Technical Applications Center. He plans to obtain his MSCpE after the birth of his child in December 2021 and continue pursuing his interests in the fields of software development, data analysis and machine learning.</p>
        </div>
        <div class="col-lg">
          <img src="img/profile_jacob.jpg" class="rounded mx-auto d-block my-4" style="width:96px;height:132px"> 
          <h3 class="text-center">Jacob Goodman</h3>
          <h5 class="text-muted text-center">BSCE</h5>
          <p class="text-center">Jacob Goodman is a senior design student expecting his BSCE from the University of Central Florida in December 2021. After graduation he will be joining Intel Corporation in Folsom, CA as a technical marketing engineer, specializing in enterprise SSD products. As he continues his career, he is considering pursuing higher management in technology and returning to a university to complete an MBA.</p>
        </div>
      </div>
    </div>
    <!-- Read in required scripts -->
    <?php readfile('./html/scripts.html'); ?>
  </body>
</html>