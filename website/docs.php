<!DOCTYPE html>
<html lang="en">
  <!-- Read in html head -->
  <?php readfile('./html/head.html'); ?>
  <body>
    <!-- Read in navbar element -->
    <?php readfile("./html/navbar.html"); ?>
    <div class="container mt-5">
      <!-- PUT DOCUMENTS HERE -->
      <h1>Documents</h1>
      <hr/>
      <table>
        <tbody>
          <tr>
            <td>10 Page Divide & Conquer Document</td>
            <td><a href="doc/DivideAndConquer.docx" type="button" class="btn btn-primary mx-4 my-2" download>Download</a></td>
          </tr>
          <tr>
            <td>SD1 Final Report</td>
            <td><a href="doc/ProjectDocument_SD1.docx" type="button" class="btn btn-primary mx-4 my-2" download>Download</a></td>
          </tr>
          <tr>
            <td>8 Page Conference Paper Document</td>
            <td><a href="doc/SDCP-Group8.docx" type="button" class="btn btn-primary mx-4 my-2" download>Download</a></td>
          </tr>
          <tr>
            <td>SD2 Final Report</td>
            <td><a href="#" type="button" class="btn btn-primary mx-4 my-2 disabled">Download</a></td>
          </tr>
          <tr>
            <td>CDR Presentation Slides</td>
            <td><a href="doc/Slate_CDR.pptx" type="button" class="btn btn-primary mx-4 my-2" download>Download</a></td>
          </tr>
          <tr>
            <td>Final Presentation Slides</td>
            <td><a href="doc/Slate_FinalPresentation.pptx" type="button" class="btn btn-primary mx-4 my-2" download>Download</a></td>
          </tr>
          <tr>
            <td>Final Presentation Video</td>
            <td>
              <div class="btn-group mx-4 my-2" role="group">
                <a href="https://youtu.be/uEN7eDD0WiI" type="button" class="btn btn-danger">YouTube</a>
                <a href="#" type="button" class="btn btn-primary disabled">Download</a>
              </div>
            </td>
          </tr>
          <tr>
            <td>Final Demonstration Video</td>
            <td>
              <div class="btn-group mx-4 my-2" role="group">
                <a href="https://youtu.be/Vke79QplP44" type="button" class="btn btn-danger">YouTube</a>
                <a href="#" type="button" class="btn btn-primary disabled">Download</a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Read in required scripts -->
    <?php readfile('./html/scripts.html'); ?>
  </body>
</html>