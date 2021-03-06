#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

''' STEP 210: Locate And-ish, Or-ish and Inverter-ish elements '''

import sys

import numpy as np

import schematics as sch

import templates

OR_ISH_50 = '''
     ------------------------
 #################-----------
 ###################---------
- ##------------- ### -------
  ##--             #### -----
  ##--               ###-----
  ###-               --##----
   # -               ---## --
   # -              ----###--
   ##-                --- ##-
   ###                ----###
   ###                -----##
'''

OR_ISH_SCAN = '''
             -------------------- -        - ---  ------ -                 --------------------- ------------------------------------------------
               -  -- -------- - --          ----- ---- - --                    ------------------------------------------------------------------
                        -                                                         -  ------------------------------------------------------------
                                                                                      -----------------------------------------------------------
                                                                                           ----- ------------------------------------------------
                                                                                           ------------------------------------------------------
                                                                                             -- -------------------------------------------------
                                                                                                -------------------------------------------------
                                                                                                -------------------------------------------------
 ################## #   ##  #####################   #############################                   ---------------------------------------------
####################################################################################                 --------------------------------------------
#####################################################################################                  ------------------------------------------
#############          ###         #   #  ##  #########    #       # ###################               ------------------------------------------
#########                                                                        #########               ----------------------------------------
########                                                                           ########                --------------------------------------
 #######                                                                            #########                ------------------------------------
 #######                                                                              ##########              -----------------------------------
  ######                                                                                ##########               --------------------------------
  ######                                                                                 ##########                ------------------------------
   #####                                                                                   ##########               -----------------------------
   #####          - -  -                                                                     #########                ---------------------------
    #####         --- -                                                                        ###########             --------------------------
    #####            -                                                                           ##########              ------------------------
     #####          ----                                                                           ##########             -----------------------
     ######        --                                                                                ###########            ---------------------
     ######        ----                                                                                 ##########          ---------------------
     #######       -- -                                                                                   #########          --------------------
      ######                                                                                                ########          -------------------
      ######                                                                                                   ######          ------------------
       ######        -                                                                                           #####         ------------------
       ######                                                                                                     #####          ----------------
        ######       -                                                                                             #####           --------------
        ######                                                                                                      #####         ---------------
        #######                                                                                                      #####         --------------
         ######                                                                                                       ####          -------------
         ######                                                                                                        #####          -----------
         ######                                                                                                         #####         -----------
         #######                                                                                              -          #####         - --------
          ######                                                                                            ---           #####          --------
          #####                                                                                             -- -           #####           ------
          #####                                                                                             ------          #####          ------
          #####                                                                                             -------          #####          -----
          #####                                                                                             --------          ####           ----
          ######                                                                                            -------            #####          ---
          ######                                                                                            ----------          #####           -
          ######                                                                                            -----------          #####           
          ######                                                                                            --------              #####          
          ######                                                                                           -------                 #####         
           #####                                                                                          -------                   #####        
           #####                                                                                          --- -                      ####        
           #####                                                                                          ---                         ####       
           #####                                                               -                         ---                          ####       
            #####                                                              -                        --                             ####      
            #####                                   -                         ----                     ----                             ###      
             ####                                                            ----                      ---                              ####     
             #####                                                            ---                       --                               ###     
             ####                                 --                           -                        -                                ####    
              ####                                --                                                    --                                ####   
              ####                              ----                                                    --                                #####  
              ####                             -----                                                   --                                  ##### 
              ####                          --------                                                                                       ######
              ####                          -------                                                                                        ######
              ####                          --------                                                                                        #####
              ####                          --------                                                                                        #####
'''

if __name__ == "__main__":
    sheet = templates.Template_Sheet(
        "orish",
        sys.argv,
        templates.string_2_template(OR_ISH_50, reflect=True),
        templates.string_2_template(OR_ISH_SCAN, reflect=True, black=-2),
        0.500,
        0.200,
        #type_pix=(150, 155),
        #type_window=(80, 120),
        #type_list=("F00", "F02", "F08", "F10", "F20", "F37", "F51", "F64", "F86", "F260"),
    )
    sheet.load_raw_image()
    sheet.load_proj50_image()
    sheet.match() 
