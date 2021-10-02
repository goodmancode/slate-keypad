<!DOCTYPE html>
<html lang="en">
  <!-- Read in html head -->
  <?php readfile('./html/head.html'); ?>
  <body>
    <!-- Read in navbar element -->
    <?php readfile("./html/navbar.html"); ?>
    <div class="container">
      <div class="row mt-5 justify-content-center">
        <div class="col-4">
          <img class="img-fluid" src="img/slate_render_transparent.png" alt="Slate PCB render"> 
        </div>
      </div>
      <div class="row mt-5">
        <h1 class="display-1 text-center">Slate</h1>
      </div>
      <div class="row">
        <h1 class="display-6 text-center">A multi-input programmable wireless macro keypad.</h1>
      </div>
      <div class="row mt-5 justify-content-center">
        <div class="col-8">
          <div class="card border-danger">
            <div class="card-body text-center text-danger">
              <strong>Under Development</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Read in required scripts -->
    <?php readfile('./html/scripts.html'); ?>
  </body>
</html>