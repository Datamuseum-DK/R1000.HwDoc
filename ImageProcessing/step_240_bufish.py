#!/usr/local/bin/python3.8
#
# NB: We strive to use y-x coordinate order to match numpy's convention

''' STEP 210: Locate And-ish, Or-ish and Inverter-ish elements '''

import sys

import numpy as np

import templates

BUF_ISH_50 = '''
--   ####          
---    ####        
----     ####      
------     ####    
--------     ####  
----------     ####
--------------  ###
'''

BUF_ISH_SCAN = '''
                     ----- --               -------------               -------                       -------          
-- -                -------------      ---------------------        ---- -------                  - ----  --           
---                    ------------ ----------------------- -  --- -------------                  - ----- --  -        
--                      ---------------------------------------------------------                -  -------     -      
--                        --- ---------------------------------------------------                ------------   --    -
-                          -----------------------------------------------------                 ------------ --   - --
-                            -  --------------------------------------------------                ------------  --  ---
         ######                 -------------------------------------------------                ----------  -- --  ---
        ##########               -------------------------------------------------              ------------ -  -------
       #############               - --------------------------------------------                ----------------------
       ##############                --------------------------------------------                ---------------  -----
       #################               - ----------------------------------------               ---------- ------   ---
       ####################               ---------------------------------------                ------------ ---    --
       #####################               --------------------------------------                ------------ -  -  ---
       #######     ###########                -----------------------------------               --------------- ----- -
       ######         ##########              -----------------------------------               ----------- ----- -----
       ######           ##########              ---------------------------------                  -------- -----------
       ######             ##########              -------------------------------                ----------------- ----
       ######               ##########               ----------------------------                 -------- ------------
       ######                 ###########             ---------------------------                 ------------ - ------
       ######                   ##########              - -------- --------------                ------------ -- ------
       ######                     ##########              - ---------------------                --------------- ------
       ######                      ###########               --------------------                 -------------- ------
       ######        -                ###########              ------------------                ----------------------
       ######         --                ##########               ----------------                ----------------------
       ######        ------               ##########              - -------------                 ---------------------
       ######       --------                ##########              ------------                  ---------------------
       ######       ----------                ###########              -------                     --------------------
       ######       --------------              ###########              ----                       -------------------
       ######       -----------------             ##########               --                        ------------------
       ######       -----------------               ###########                                      ------------------
       ######        -----------------  -             ###########                                     -----------------
       ######       ---------------------               ##########                                    -----------------
       ######       --------------------- -               ##########                                  -----------------
       ######       --------------------------             ############                               -----------------
       ######        ---------------------------              ###########                              ----------------
       ######       ------------------------------              ###########                            ----------------
       ######       --------------------------------             ###########                           ----------------
       ######      -----------------------------------             #############                       ----------------
       ######       -------------------------------------             ###########                      ----------------
       ######       -------------------------------------               ###########                   -----------------
       ######       ----------------------------------------             ############                 -----------------
       ######       ------------------------------------------              ############               ----------------
       ######       -------------------------------------------               ###########              ----------------
       ######       -------------------------------------------- --             ###########              --------------
       ######       ------------------------------------------------              ############              -----------
       ######       --------------------------------------------------              ############             ----------
       ######       ----------------------------------------------------              ###########               ------ 
       ######       ---------------------------------------------------  -              ###########               ---- 
       ######       -------------------------------------------------------               ###########                  
       ######        ---------------------------------------------------------              ###########                
       ######      ----------------------------------------------------------- -              ###########              
       ######      --------------------------------------------------------------              ############            
       ######      ------------------------------------------------------------ -                ############          
       ######       -----------------------------------------------------------------              ############        
       ######       -----------------------------------------------------------------                ############      
       ######       --------------------------------------------------------------------               ############    
       ######       ---------------------------------------------------------------------                ##############
      #######       ------------------------------------------------------------------------               ############
      #######       -------------------------------------------------------------------------                ##########
     ########       ------------------------------------------------------------------------- -               #########
  ###########       -----------------------------------------------------------------------------              ########
#############      ----------------------------------------------------------------------------- --            ########
#############      ---------------------------------------------------------------------------------            #######
#############       ------------------------------------------------------------------------------             ########
  ###########      ------------------------------------------------------------------------------              ########
     ########       --------------------------------------------------------------------------                #########
      #######        -------------------------------------------------------------------------               ##########
      #######       --------------------------------------------------------------- --------               ############
       ######       ------------------------------------------------------------------------            #############  
       ######       -------------------------------------------------------------------  -            ###########      
       ######       ------------------------------------------------------------------               ###########       
       ######        ----------------------------------------------------------------             ############         
       ######       ---------------------------------------------------------------             ############           
       ######       -------------------------------------------------------------             ############             
       ######       -----------------------------------------------------------              ###########               
       ######      ----------------------------------------------------------             ############                 
       ######      --------------------------------------------------------             ############                   
       ######       -----------------------------------------------------             ############              -  -   
       ######       ---------------------------------------------------             ############              - ----  -
       ######       -------------------------------------------------             #############              -------  -
       ######       -----------------------------------------------             ############              -- ----- ----
       ######       ---------------------------------------------              ###########               --------------
       ######      ---------------------------------------------             ###########              -  --------------
       ######      -------------------------------------------            ############                -  --------------
       ######       ----------------------------------------             ###########              -  ------------------
       ######       -------------------------------------              ###########                ---------------------
       ######      -------------------------------------             ############            -   ----------------------
       ######      ----------------------------------             #############               -------------------------
       ######      --------------------------------              ###########                ---------------------------
       ######      -------------------------------             ###########                --- -------------------------
       ######      ----------------------------              ############                ------------------------------
       ######      --------------------------             #############                 - -----------------------------
       ######      -------------------------             ###########               - ----------------------------------
       ######       ----------------------             ############               --- ---------------------------------
       ######       -------------------              ############             ------ ----------------------------------
       ######       ------------------            #############              ----    -  -------------------------------
       ######       ---------------              ###########                  - -          - ------------------- --    
       ######       ------------ -             ############                - -  -                   -----------        
       ######       ------------             ############              -- --                         --------          
       ######        ---------             ############                 ----                           ----            
-      ######       ---------            ###########                     -                                             
       ######       -----              ############                    ---                                             
       ######        --              ############                                                                      
       ######                      ###########                                                                         
       ######                    ###########                                                                           
       ######                   ###########                                                                            
       ######                ############                                                                              
       ######              ############                                                                                
       ######             ##########                                                                                   
       ######           ###########                                                                                    
        #####         ###########             --                                                                       
        ######     ###########             -----                                                                       
-       #######  ############               ----                                                                       
        ###################               ------                                                                       
        #################             - --------                                                                       
         #############               -----------                                                                       
-        ###########              -- -----------                                                                       
--         #######              -----------------                                                                      
---                            ------------------                                                                      
---                         -- -----------------                                                                       
-----                     -----------------------                                                                      
-----                   -------------------------                                                                      
-------             -----------------------------                                                                      
----------          -----------------------------                                                                      
-------- -    -  --------------------------------                                                                      
------------  -----------------------------------                                                                      
'''

class Bufish_Sheet(templates.Template_Sheet):

    def validator(self, target):
        for x in range(119):
            if np.amax(target[:,x]) < 0:
               target[:,:x] *= -.5
               return False
        if np.amin(target[20,:60]) > 0:
            target[20,:60] *= -.5
            return False
        if np.amin(target[60,60:]) > 0:
            target[60,60:] *= -.5
            return False
        if np.amin(target[60,:60]) > 0:
            target[60,:60] *= -.5
            return False
        if np.amin(target[:60,60]) > 0:
            target[:60,60] *= -.5
            return False
        if np.amin(target[60:,60]) > 0:
            target[60:,60] *= -.5
            return False
        return True

if __name__ == "__main__":
    sheet = Bufish_Sheet(
        "bufish",
        sys.argv,
        templates.string_2_template(BUF_ISH_50, reflect=True),
        templates.string_2_template(BUF_ISH_SCAN, black=-2),
        0.500,
        0.200,
        #type_pix=(194, 196),
        #type_window=(50, 90),
        #type_list=("F04",)
    )
    sheet.load_raw_image()
    sheet.load_proj50_image()
    sheet.match() 
