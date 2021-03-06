#!/usr/bin/env python
# coding: ISO8859-1
#
# Copyright (c) 2013, Preferred Infrastructure, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
maf - a waf extension for automation of parameterized computational experiments
"""

# NOTE: coding ISO8859-1 is necessary for attaching maflib at the end of this
# file.

import os
import os.path
import shutil
import subprocess
import sys
import tarfile
import waflib.Context
import waflib.Logs

TAR_NAME = 'maflib.tar'
NEW_LINE = '#XXX'.encode()
CARRIAGE_RETURN = '#YYY'.encode()
ARCHIVE_BEGIN = '#==>\n'.encode()
ARCHIVE_END = '#<==\n'.encode()

class _Cleaner:
    def __init__(self, directory):
        self._cwd = os.getcwd()
        self._directory = directory

    def __enter__(self):
        self.clean()

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self._cwd)
        if exc_type:
            self.clean()
        return False

    def clean(self):
        try:
            path = os.path.join(self._directory, 'maflib')
            shutil.rmtree(path)
        except OSError:
            pass

def _read_archive(filename):
    if filename.endswith('.pyc'):
        filename = filename[:-1]

    with open(filename, 'rb') as f:
        while True:
            line = f.readline()
            if not line:
                raise Exception('archive not found')
            if line == ARCHIVE_BEGIN:
                content = f.readline()
                if not content or f.readline() != ARCHIVE_END:
                    raise Exception('corrupt archive')
                break

    return content[1:-1].replace(NEW_LINE, '\n'.encode()).replace(
        CARRIAGE_RETURN, '\r'.encode())

def unpack_maflib(directory):
    with _Cleaner(directory) as c:
        content = _read_archive(__file__)

        os.makedirs(os.path.join(directory, 'maflib'))
        os.chdir(directory)

        bz2_name = TAR_NAME + '.bz2'
        with open(bz2_name, 'wb') as f:
            f.write(content)

        try:
            t = tarfile.open(bz2_name)
        except:
            try:
                os.system('bunzip2 ' + bz2_name)
                t = tarfile.open(TAR_NAME)
            except:
                raise Exception('Cannot extract maflib. Check that python bz2 module or bunzip2 command is available.')

        try:
            t.extractall()
        finally:
            t.close()

        try:
            os.remove(bz2_name)
            os.remove(TAR_NAME)
        except:
            pass

        maflib_path = os.path.abspath(os.getcwd())
        return maflib_path

def test_maflib(directory):
    try:
        os.stat(os.path.join(directory, 'maflib'))
        return os.path.abspath(directory)
    except OSError:
        return None

def find_maflib():
    path = waflib.Context.waf_dir
    if not test_maflib(path):
        unpack_maflib(path)
    return path

find_maflib()
import maflib.core
#==>
#BZh91AY&SY#XXX �� o����\������������� @H  �`k���M��6���'|��y97��VY]���锄�( ^��� ������>(�B��F�����>��w��r�{���  ��]���M��e��{��^�����׍M{}���N��龀 |�������K{����W�&���6y޻�!A�n����w/lTlj���C�����g��^Ǩ����rCf6͚��y�n�@8�ѷ{�J��������ϣ�N�؊Ѽ����������j��{���#�^�M ���&MOP�I�=L��Ɋzjz��� �=@M %4A	�i�&F5@�#&� M  A""hS�4�=���S�=G��4�F�P #YYY#YYY  #YYY  �I"�h4��&�&�)�fSLC�Pڀ4 4h��@CDi���������Ojm��)�=�cB����������QD@�1@L5h���5M�G�ښ44=OS�z�Pz�P�d��/�p�� �u-�̄&b�|>E(\1��~OOǒA�E��a���X_�w��X�A�� Ĉ�Ŋ��P�,Q$�����޿d���v���b��:C��=����L?�=�����}�v�mq%ih#XXX��h����������?j��	�k�;#\^'t�3J?�����+W�vu|^�q�a+�UX2Cx#XXX��̋��0�?��vw��.Ɇ�gL#XXX�s�V�	�&����Mj������zc��Ԇ#YYY�3�p�G;g��}��(I�<=f<�,?E�S����1�M4��n�r��؇Rn=��sQb"���@J�3`%�ΐ��+�h����6��Ë�y#XXXa�e(X���(��&��P>�߿_�y��r����c�#XXX���e�G��� yg'�t��f1�5�'�B��>~|哒ւ�����)P3z��D��9Wŀqq�Г�!6�9r]*�YK�W�3����������1���bp����|J*����v�N�8�k���9m��9�vh�����7�H�[A�ڗ�&�.����n�����b4'��+z�T_�m�����%���{M%���,��^��Y5ņ�Y�rNjv���8z]pG���|Pڤ�����P�dQ�`���Kη��9|WTG�y��k���a���~W�����~=�3Q�w\�Lh�[H�I#XXX�����=7�{O2p�}ɖ%g����H��uyx��t�������f˾8I�K�+u<�5������Ƣ���g��SA�@�'B�y���<�]�`~�`��Ɩx`p�@�e��*2E��x�V�0<�|T���V�f���s���������r�~�U>,�!��LպVo߯&�������H����필k�Ld����'�v.���I������ԝ�'�~�H�8C�K��QX��0����̡n!��TF$��\�f붆#XXX�C�9H�9�r�g[?JF�$���>��aw�N?(��Q���JWN�X �u�O������Z���)���v��Oa�|:f���_�d֓����$Bo5r�Ԯ�GH��5�c�����v�O�bX�#XXX�E�� �8$����0J �A��sL��7��ݽ`3�M��j�L��B=��zϵ��Y����]}3�y2��U�YP`���T3�_���mHh�����z����4�O��(&7o���H]�8W��a�]�x~��Q���o���x���p\97���jg�U��pkZ��r<9��/����p��<GQ�O���,��k�\�k�����3�0�yh�dJ��Y�˺ �#y(K�U#��i�&އ�9���]��؁Vݹ�D�����#YYY�����t�Є M����T�*b�����77�A0��g��e���GY�_jĻ�q!Tޱ�pl�b�i13/U�<k��)���J� �{;F9YL^L��WGgY|'����;�R��i#YYY?DE�p.F\:U(�z�b�ox@O��A���}g�?a�����V�m��-�^}�pp7	��sa�,?p	�����g0�l����G��:����>6��3����ˬ4��D��@���M���<�f>�>@��7Q��#YYY���;-l��l�t���Q<z�g����q`�q��ֿq\j�\]8�k�ɢ\m˓-T�=:Y�h������42q<�����L�F���q��}��l��+F#YYY�r#�-����5y��<��$	�4ϳ�n��`���b8�n�NuǱlZ�w��܏pp��h"RFM3�N�7>M��o��������'�#YYY�d4'>����0���j�M}��-X9>���#XXXA�����[��ޯ�]ֆ7n5����0�d=-s��r_t(��#kx��u��iZΏמ�8�����&�Κ�1�V-qV�a�#YYY�ɝ��4+Z�����.�pg��u�L�;#A��0�I�[�(�����N�Lj]�l��T��ֺn���y�>]�+��G�)�2/����S��>Mf�Z���81ed<�N� ��@��J�O�W�T��\��"T#XXX�>�l�ͩ���n�����:4x���Y��#XXX��b��ǇC���//����FSL�������ޚ�l���|�;s{e��Ђ�$y�G*f␐��s��f���W<�"'5;{�9�,�$�GC��ބ��>���%�����ݻ�I0%��|x��|�h*3��6��2�#YYYKb��G�̥� ���� �	�ޱX� Xu�b� �b@�!O�K]L�ƏS�����s�ɬs�`��ځ� �N��l�8j��m�KzkWS�^#ǶXޭn�j�N��f(�=��zDӁ���ľLZ�(^e����/	R�1k�Bd��)����G{��5 p'-��څ�%	?��v>� j�P�E\�5�:�96 ��P1���j뚉^)�(�L�(�Є��(ϓd(._��}���ߺcu�p�s�8��il���b�rS�*�J�ڪ�/=���Z��{�DCz�t����\v�����:�#��>���~��%�H�������؇�Mⴡ���`��qE"e����e�p���=�GR��c�9  ��S�Z%aG(\w�87g�ጚ��	���e��m�ĎKRȲQ�Y9���ר��ƪGC3����ó�˃��"27�Q��J�-s<TN���V�+I�<����/@��o��E�u��i�]##�NCMj��wǾ�e��f�G�"��P3p�ͮļ.�D-����(PD�O�t�z�ڣA���;;^�Q��cƊlmΦ�B8��rd����t6�y��rS~�3��I秸*)�{���	U�NO���M��E*��Ps�#�E/ap�P���2�#XXXCޠ�JM�f�{�,xJ[��1��9��ʹ-~��F���ZL�e�ݓT�rP\N�fm�@�fe"�a\��])�GY��kex���>����Z����]�����+!݃I�2Q������7�q�����)ʯ��2P��R*�'<�3�hM�1���1��:�%�čƑJcn����$(�lÔ,bc��gS���ۓ5�,Rɾ�>�vͯC��z���������/=,��#XXX�F:q�8�i���i�ku�(ۏDv���&��8��b%�w��`;��F�W�#XXX�^�4���Bmb�o��8���#XXXF:������(m{������s��Lv��z|���wϓ�z����tl9ǏMm��gi�d��S7(��s{�%�Sr��'n���\��軙�Yj%4��]2�fy��L�t�g[#���r��z�My�Khq����!���/=��B�F|������P��0q�c��]�C$q{*z��YF�gN��ZE����xw�K|���#?%htQy3��Y=�Nn��R!��&P���"i��m{�x���]i�BtB�ʗ|T��᝭>ʎX�b������J��\��#���3�=��q7�ʐ|�6#YYY��r�cG�:���7~���e��y�CW7���Dn1>�vַ��uh���؉��li�+����u����J<����[|1���j�D,����dt<��T�)x����l)0��w��ٵ����a�yҲKwd�	t�a�>�ۂ�O���������N�0�[3��ŝ��(�<,]]ޅz�X�$KM\�Mx���!r��w����<�#XXX��ywy�*|�������b��c�ހ����B���fэ�/�����EORxf:5�I�Ʉ&wg��6��7&l=��+��g#YYY�r˾5�i"Hߺdz�����&v�ԏ�;ד������9L��1�.35A�i�[E{�B��im�/mr�!S�6�h��.��gb[U�_gB�]o��nq��pz�ˎ�X0����VtR _��5�sPdpΜ���t�ݐ�P)�b�����:�M[��˓��Bp�M���^$��Y�I���lVR������B�-.�J���=���P�+�І�@M�i�0�<�b�9E[ż�oG"�r7��>f�Q�l>��#YYY�($��`�10.Sj#YYY�O�@��	��)�8��@.:o鼻���c	�N��iT�(�F���4��TN�/��x�i�����Ruv�0�^�`���L]�7�6�4��+J�sk.��UKjp���l�k���/�R_;�*��8��X�-�mE�����E���2kH�h})Z�%ĻSӐBi�#YYY��z�<�s]�D�6���c�E�$K��#ӚE�$f#YYYc�yd|���vH�m��~��W\w��(�&�G4v�蹉i6�(�ⶫ�T.�^��Â��]8�c,>O��c���cɳ�����P�%Al ���#�1��2m�h��*��k<�������S����Թ~�z��7\��dh�ͳ���5w�|���[�o*>x����I�#XXX�\8�JI�j�vӤ*d�f��l$x;����H�l��;ڀ����`�D��i�,�&�,����U�Ƿ�`g���x�x {a��x��뿏-�~�{m���n$����Yg��x�*�d1�XFHI��~yLc$�8�����}�#YYY� �xχ2>xp���9-�ô�*0�u:�z�1���q�u���'�߁2�5mq����F*���8���a�.�>�m��A���=��@��O�g #YYY��A��A�´1���ٙ��HF�2C1������c0wA�s�e6�4L�ӈG�3����>/I�nw�HZ2��#XXX>�\S�G�������{l���8wn���W�K��6J�${��t�kt��<�{�Ó�,=?O]w��~�������}�V�c�r�T�S�0E)�9�/��9�@x+��]�*���<_�D��k(��T�h�RkVݯ��0����C�f\j�4�M����-ϣ�f��:MxaTf3G�K����m��>�w'rkJ�i��?T�*�f��`����f����ٖ��#����+�C􍐈;��u2*8�����h���ϯ��p�5���^�D�L#XXX=	nc���'K��8�4]�?��֢>�<�9��OQ.�4�K��#XXX\��%�~���I�2��:�y7�6c�A��24)6���Y4�'x����9֙��^�r���j�0k���s0���II$q���h��s">�|����		�U�b��ܝJ�w���ݙm��7?$�y�Ѣ%�#YYYa��k!?�c}��5{��5\��gjc���Zyzj��ntV7M|�\�g�q5?�h���^�Ttvql�E���KukU�N��Y�9�0�֒�Y�dN9E�#XXX�XK(2����%�f.�RԚz#XXXk-tֈ΄-lEo�=�+Ü̎1k�}>�5�G�AB�{:����-:�������Z�L���ϝ�u�LOs/�d�'K�oZ���i��}���r�и�>��%P����H�sq���w�)%V���{�F�f���R�Yl��龗�r�H�<-(a	A���E7YT�J�fS�.�Z���ss��;N��(9������N6���C��(� ��#XXX��An�Qr��#YYY'H��y���Ua���;�|�K͇N=�#YYY^4>_�t�䟤?�l�����}��6�+ :����N�Q��Ӂ��$�y��Grs6���c��(�8��p-������2�9��q0B��%Ժ1#XXX5�CpU�G���U��@��#���n�eHvuo" �x�ݵ��ꢸ�ܹPn��x(1�����S��h�j��/C��Ԏ����Pb!��+.��7�\�t�n�P�	5n�������;������Ŋ1�[��U�N}V�����^dзMY��jp������vCV8�����;��K&e�&��yG���؞����#XXX�����o�cad�����TN.�N`�x�߇?�{����>f돰NM>�������C���۪�����W��=�>	�UUUĽCKY	L�i˧� >��~����?9N����G�)�'C���o;�yN���=VE s= 젃@F�3�\A�tj���#�|=N:G$;?��6��H8���c��뒅W9����ǀ7��v�;8Z�n#XXX`��!�/�&�:f��k`�����M*��saZn[y�F_5̈ᔵ��u��d�����z�Y{�@j�p^(􃣣m���-'�S���~���-s[ȮR��=l�Ž��������"1�_�s�%��}���`�#�j^�Mf�F��-=c� �4��s'���A�D���*Ϟ|�D�'�0�ȋpP~��qU$)P@�#Xd}gΒs��x����˾��i���&ͻ��!�*�2yj��+JF�b[���X#XXX]_+Q��y��n�7+�EŠ�W�r��s�������Ď6��Lkޟ��ML�s���Q��Tɛ}WWuڣ�rm'����a�_PkSۯU�O2N4���$�T^�s;��z�)#XXXS��뢝�z��rD�%�o�ZR�G��4�]f���0���)�'�#XXX�>!�w�P�7�'1#YYY��7rg��|lN����l����.5�D�S�m=;����`�-&�ϤU=��a�C��C�ֹ�.z��ļd8#!����[ˤm����h�<ܝN���(rd	a�HZ>c�Mp��ҖF���.M:�e����ܯ*��bq��+��8L�C��Ϭ@���㌶��ّ����h��<��3pNز	����Ʉ [��	~�K�{~׋��OP[�!�D�0�-Wn�8۱���[�J�3�f�d�y$(zןX'g��n��3$<����JT�/�v�d���0#YYYк<��W�_sx��}Mv��>���8x6s���%�#<�#XXX+�=���U�:c"]��'�������(�/�X}��/�mw�E�������Q��|����S�V4�����⟱F#��aA��\F�I#XXXPX�h!��V���ۡ�#XXX��.�g����9�g0{��_��`l�Ph�F�՛6=�#YYY�W_���ڷysf\�ta�1���T�qDbvfCk�6B]u\sמ9F�F ~�Z��[�'=9x��_�B���ʂ�&QRD�GL_�h+�i�hXL����>���6����Ƌ�ç)�ȕNp�[����u�\PD�m�9��s����K)��]���]���q	]u��S�k5]h�.;�:#XXXey��l﷫EB#XXX�lS>��="V�A�� ��\��������E����i��R#G�-�+�׉b(�T����D����T'��R(�K(�a��B�«�o�qz�����L_^˻�uA؁�(Gi	s��r�4������4.i����{���B8Y<�T���R,DcADI�*�J��d�@A� �+Rs?@|x��n0��h~��#XXXHBD�#XXX�BC�?�d��C6Kd���a����8#������~�&U!���jZ���#YYYؠ����s�o������mx�����U�qw@�_�2�go�`�\g�c�?�O����j��``�0#XXX@�G�8My?&?�n1�����t����|V*[�;JO���(��vFMb��6;O�IAl��:�������|3��R�Y�|n��SS��?"n<����bFt#XXXQJR0Nc�;ɩ��Gq���8�w�)��O)�{L��S'�M^�#C�SA�=�q����N�#YYY���q50jl8�547Ga�:�N��X����_ϫ����٥�o����rA�?Q�i˝��+�N^S�`Am����|l������cx�N�-Q�e(��w��'��w^�Q�)���R|��946L����#YYYMF���##A=B���O#&�#�S#��xp�q#YYY߉d�-�Ǔ������i��n8�^��>��<��c�#YYY�#YYYĮ���s�$���a���F�8k;�U�6v�#XXXo)�l~�l��:��#XXXyJ�{$��mJl)��Pׄ��i�}�u�T����Y,�8�i}��s*d��=��41'i�c�`jdRN�zOYN�j8�O7�4����[�r���q�N�'�Rx�n�}U�rƋ�r�����4��QG��'��55'�r<��(��Z�yJ0n22d��qI�7rLJ_v|g�F#YYY�La�29�:���F�CC#�$�ᴥ5�M	o�z\/'��U���;O�{�#��R�on��4��';M�EC���'=��jj=↎|ʱScь>��O��m����Eb#|m#XXX��oߌ_����7�+�v�x��O�z�AM�AF��}T|����T�I��x����MJl7a�M�a�N�A����7l����Ty��_������U����a�����rW�o�N����0Ά��s��Y��s�ـE�Ԇٍ8��|��������SL���M#XXX��N�F�~#XXX\�x���cd�3��wW%��li���ty`u�ſ�����Σ����T�o���^����dL��|Ύ�K�������ñ�q��F�km|O���C�ð�~8��|���p���h����?Q�$:9sG���0�u�#������5?��:���*���}by�?�����9$��D���9�o�J9IF�K8	ђ%'����}afz���F�o��k�~ǧ�2I�`�z9��vA<�t����ڦ���W�v��b2BW��.����w�C����S���B= ��`#Gn 𵸏u73 I!�������kB�����#��8�&V�q�)��!�-���980��l���㪁�|E��|��#XXX����e��1�F�P>;G��vFT.�D�vKk/m-S��i���ĥ�A!#YYY�����kv7������;���֔[F���q4tm5 �/7dC�����%-��u�I��i�V��I�]F�s��~}�xzz^�͓����q�V�C�y��T�j��s#XXX��A�+���,4'c� ����JZ/�����q�F�����vh�27�a$GG=t�!d���P��i�js�(wNW=�B��p�6s�Y|*�eBY%d�����^�����'��{��mBT�Zl�+V�2��6�V��`t�-�߀G��T�D�z��kR���gݎV��5Jۿf��!ʕI#����ǻG�Py�.P�w��-���;����rf����d�d����4�1KH�-<�Z���y³AHF�VJʓQ#YYY0l���#XXXB<i#XXX���`��@�%`#XXX<�'�>d>t�I z! 2}_rf�g��c��c��$��ܳ7mف�A���!�UQ�x����`~p��Q��a@�,-(bxR&>~����buȢ��_��)US�ܛ�y���A~��T��� dINg͸# �{J4��#XXX�:��Z���]����'Xѥt��s������fGMf������1�#XXX-��ĩ*q�D2S_ �$�lM#XXX�Y��F��tD���*�2��flp��ap�I�0�ܑ�� ���T���4Id�"�-,QR������,��F#XXX8�N�$��B��T_4#YYYP;�:\E~��e��S@��CZ�#XXX}���7p������ˢ��x w�dT�dBXER03�<��8�:`�)�B���U^��%T^�]yW��:��o2��S�8.�v��4%@j�4߆ɜ*'EQ"�18Ĵ�pd����$�PX�M���a�eYZ�ZU�հ��J��,��ա����j"�J�c�Nf�{��,�nh�R�&�K�	!�L��"J���v��}^�5	46ؙ�Kh��̖����S]-rC�T�6���xi�}~��8S��\;���8e�<3�d$�0�&w�����J��O t�k�Y��}T~��e2i�0�6��� ���j��3x?c�=��N����'���"W^�vC�D�"䔿m�]�Z�4arm��c���0}�>ؤ��!������M5����#r\/�[e*�7�1��)�^X���,���l�UHi9�,;#\�;�&,�֙�K�/�K�1�!���x-��CPR�ЉP%	K���h+D����*���K��/D��4�i�.Y;��fN)sS^��I�_��@Y_'��+��b��*� �䌂ń��d�	�Ao[��\��.!�c)dX*ŕY�K�y�����C�xx& �f�V�6&���RwIx~U�`���^D}b��%���]4��g�h9*7d�� Q����f�H��^��c%�.�N׵���:fa�4���ȟ�`� ;[LW�걪h��*I��=����d�I����1�#XXX{;B���PU��1�f�*e��E��D�B) -�f[lD���a�cЉ�Hb�,��,#YYY0�UE�9��!�K@�$S6Ff�8����d,�>4�ʵXk�,&�Ї�M����C�H�g��2�� ���V����������0����j5#78f�k���qFF(Hީ�ɀ�6�%���e�i�MM>�NsQf5�,���v�H�O�8!����:;n�S*a��\�a��������Аw�0P��i'����*��w�#YYYK��4�$���0*!:)�2��/�T�I��h�JS��=��nS���CD֢[>.���F,�	#YYY�WՌ8�=|y9i�N�0�;z��岨�|IZ�Ζ`��6���ՠ�˔�f�K����ڬg9����N; L��_ܞ��N�ƥ������ٌ1�!�`f77H�p����&�-�0˥ "���g��ƨ�V���vB�"�.�\�����@ڻ�-���:!�Ɣ�gG�܏�ábt��WK,��Q��A�v��j~��kP��ˏm�m�Odp	�8�S�ۄ���a#XXX�ϓ*�B���#XXX4���O�;��Ƨ��\�|g����+v4Q��*Gܗl8����}Ĳz|U��a��"�	G	��"��ډS�6�wӒtOA�Tj.�$<ΛI���#NNQ�l�߅�|���Y��a�u���{Ә:t�wgB(0Y�w'�щ9M��r��I�F���Z���	�a�Z�k�@�l���D6T�N��<ER�gn��œ{�#YYY��m�왺�dvf���O�XMyĚ�?^�Cp�$S�R�8z3������L%���8S����YL���]��pksHv��#����"W�9��e�Mr���gf���l�d���^3C��l.3;��=�K��ߝ\����9�Y�0�Nn�����˟�j�r�D�y7�a6rCDޝ���a� 옙&��F�;<C6�"^W6N�vrt5ro�ۙ�Ɣ"�_u;��N�,�|#YYY�ŵ,�R��<,�,�\#YYYMH�07D>��c���I!�N_�h�	��*��<�+i��9k�����c�ʮn��"���2�|]U.j�#ZOe�;tÄ,[���&Z�z�I�bD�18k.�#�0�����.�E��*S��G�4B�A�y�);Xb��lL����]�xwZ��Bb�����8@�w�r�l���eКisM���/��F"����ngy;��n��2YN�N��.��.�E3���i3	/2��j*5/�b�d�խ���]5<d����"�k4&�ޡ4�������jF�8���z��_L5�2���,�C�8h+L3�EM[^�|�)K���6�y���4�����N܊x.��	`]�a�j����5h}Y&��%Az0(�Y$��D�PZH�@��Fhlz��Re�{��<�l(�~4d�eɄ�H��1P��'�s��)Z��=��G�k�qx<.��!y6ڛ��98n8��#V��҄�l���S�jk+rh�̞;��-�m_���6��I�9l�ǕOo�gq$6�D�@�O8�2k#���7���q�6��(DB)0�aA��h�.D�����Q#YYY�6b�՛���뵃#YYYF��6@�C@/�H#XXX(�n��C2"�kК�M���?f��6�t�F#YYY�B�è{0�a##�R��������bI�B$Ml9m�w�l�������=8�>��|\� �#$���V�#XXX=ݚ��,���i���PL��j0�R`��H�ٌ��yu���֟&�f�>k�K����z�YX�Dr������/�b+���U�����B���a�{��N���N�Ai3ra$��o6�jj�vM�}xHi	���|֖�V3��!�QF�F�0i&1B. �� E$�b���1= �i�'��4�6�>ח���vp�DT�ȅ��[۝F�0û��ݍtVYc��C�'�b�l�QR/S �q��k`Q ��bGF9�l�hV��K;,<�٭��������Pt[q\���2b$ʭ�����o��| Z�S#-��\p���L݃[s�Y���8���#XXXN�6m&6�]�2A��k��'C��m`�`�fH�-i�nF,�1:2��XX��F$�+<���T>i%H�]�f�d����Gy��X���D�h �}�*�[*�ȑSf�@�7��Q)R�۶��Q�Mc�����:��^��z���$f�:}/��5�y����|�c�#XXX�\/�|��~?�SC�Cl �_f5ȯ�.�L&�?7��gG��L�eLų쯮�����E��DD���'t$H�=sk=VT�l�Y?;�B+\�m�$ޔ��m���,`4�&�B�A�6�[l��#J�H���D#XXX�2���J#XXX.*E���Bi���4đ[��JH�����7T5A< ����!Qh"#XXXl��\�K�h�#YYY�+<oM���s�pb���dA��n���L���*ԝe����<�hTm�Gv'��-:��y͜���(t�C�l�[<Ϗd�3ި�S�,���=(��V���1lc�B�}�j����v��#YYYJV�¥n֛)�nb`��)#YYY`�ubK�K�֗W��Iw16Ys�4怰vc����X�F����?'Bv8���- l����h�HH� ���&+ (�,9���Ac;=�4��Y�LY�oC��cr52��N�*�9m�s0��4��P�)@)��&F$hw�y���MB2��U�#YYY �w�=�3q����q�l~������c�OÅ������u��܊h�d�t'd�6��*'ɟJJ�D:�E�1Q%J�J�0�Q`���@阉*I�U�$�B��,�ȡ`Ɍz�%��J.����o=d�̘B���@�`�,c,Qb�I%$ X�P��M�����o��3�֔A��}L����y&"�R��"d��PQF"��UU���J#XXX�o��6o˒8IGhi{jNY�TO/o��������	:�� �Њ�������۴)6H�����C��4���6ĉ��w���	�ڑ$QɊ����)�@>Z��P<<Ł�#m��$,:~��~� FI��!��`�!�:I�G��2��z��٢�ɐ��f��K�煮*�h�Y����d�];�W��b�X�av}���uly�dv�Kq�Q�<zgRw*�e�w#���,.�4�G�l��2	�~.�R<�Ŋ,�"�kP���`ܗˇQ�7#XXXc���>/�EGW�:bHi#YYYzl0a�������:����iBж'�*5��D,�>�|G�*Q�]��:`{�`Μ9r; �&oP^!YTtsQb�z4��a2,�(B�x��)P��{�~���j�����2p-��{���^�&&_Y���J��kIä ��Y��&�(��d։�C�<	! �ځ�6���J��ي6N�qW���5U����G����c	�+ή����Y#YYY�cѧ����'�#XXX��X�"#XXX,��(�ZE�bȲ�-�w�\���فs�D`�A�3P���0��{��0�C��(Z�x���#XXX���Pb�ϭ<�iDj�#XXX0����2[[N���<��������COH.����� �DY$X#&�O�6�V��̳#� J:lcB��u(�G#XXX.��=�Nv���c��ky�\��,�J�.;dt]��V��f��C���[�F���NVxwS�[(��~�#YYY�lz#XXX�A��g��c"Û��+���R3d-r������HÐ�6"rD1��P� Y���a�ԝFSE���p��Ly��d�T�2B2��=�s�bon�+�g:�7o.a!	(('+*"���Ɂ�{N��<�q:�k��"��k2#ehX(�	��f��B�z2��z"e��̐�h@�0� �HPJ[H���T9G���%��g��k��P>�IA��VR�v�`a|!uuJ_·An�������~�c�X�קO��z^{#��e�����;]���˦��@�IdCT,0�F�+E47��M!�p&iLm��:'w�5���pkk��I��#�SSQ2amL)h[��sV#v�Y��:��QN�D���MCr�%�v���zy��/�����Ow�r�z&�DI�Ҡ�^���tN[XyۃM7�`�P��'�ul��aaC�:z~�HL���da!����S17����E��X�ψg��*���]~_C|��Z}b*�X����E(ϴ��`,7�����1*j�R�$c�&&,���#�p�����G���֛�N��9����ko����@I��r�;��S|P�V�m��3HjDE@H�/�6@#YYY`��	���ߥ9��3�o��|�2y��{Y("Q�*Y(�)�5�3PA��,�-*$`+����M'��%�]��D߄$Ђ^�#�����D����|���_�����7�q��=�7��{`R�C>�>W�{}��ڪ}��@�N��6��䱊m��YlVۀ͐�#XXX�#XXXq������>0Ҵ�]�DCH10�(f̍V�`�U"IC#+D���G4G������C�����b�I	y{eGV�1��)gW��Mv��9Ϻ�)M>����1�]D��q����� %�%��eL��K����#YYY��nɚ@v�4�ξ�8î&8��C��΋d�#YYY��dS ^H&�V���Ҥ�a��\vBLo;���ly��5��r�&���4�01�b"�V̄1dB̘�8�m��ښ޶V�;�A�'�<��^�#XXXk�{y�F��@d��]�<�"y�_F�fh0{��X_^m��SJ�Lf;�Zc1�����o*F5-�9�Z� 4<��\8m��G#YYYU	��-7����&�D���0��#YYYF�-lX�dD��W�#YYYNޛ�y;JJ��W�{�l��PV-jW��&�қ����i0�#YYY!��6�#�P�K�|�ML������F���H��7X�X�f�ު*K��q������0�JFH�DX"(#,��%1�F!.�I�#YYY�]��LBD��XI����c4&a�@S���+|\��-L`�#XXXD�1dX�Ar�xY�%�..�V�n�����I�AtB�AQ#YYYD6�ݾ����L�S6����RئǄ��q\ē�A����(���򨤚-��#XXXe�I8�ņ�^������l��Y�.��c4�n�c3]qr��8g-��#XXX�*���	�.�J�Њ�%��1��V�,=j�f���o��� ����+ama,},	�`�d� FgD�#XXX�X��l5A@��J2h"�a"�H�F�E�ɲ��J	'��g�g�ӻ�|�!	��<�{8K�#XXXp�݉/x�G�D�ptE�>g�S�@zyS?1#����1�zP18;u�#XXX�M�,Z D#YYY�	���WL��QA/�#�LMu�9E��#"�k5-J�BHFQ������� ��\a�a#XXX0��F�Ȱ�#XXXFLBTȀ22,�"�H[����"b��;`�:��[�����a��$y�D-���`��1S��DbNd7�=@`lN�t��`���w-�P*�.Y�R$�D��bm@�b�b1d9JP-#XXX(EB"�H ����RMv�Y��e���&��EM�S]���Z�A�AHH �	� ��z�5��	�������1�è���W�s0-��d�Dca4��2 ��������kL��XbE%h��cP��q�-��a�5��ṥx���Z(�����e��0@�WWNU�lI	A&���(��o�R���=f���@(��T8.�J�1��1b��d�'�֊B'�~>���?�1�"6�~O�H����҇!m�w�z~��lu�?#YYY���xP��Ӧ��?������g��'G�A�����cqU�X%ŗD���#�T�-���������U�>�(~$0S��f#YYY���`TA&ɬR�#YYYP�N��Yy,{J�MU�0���>�/&�=ּ�ml)�B׋'=P�=4�����?vK��0����xc��5 na������2#YYY��0��(Rjp��'VWM�^�4�V�A7xD��!�rO#XXX7�JO�!����e8�#G�#XXX��F��:�2�����re[m��1ߌ��#oÝ;�YД������Rur�O�d��ct.�Z_zŚ���)�����ԕ��]��$v���-_':Ǳ���@�Z}pz%�:p��x��"��Sp�k�CXu-�k��p0�2�(�B���`#eX��7�}?j1Q �DQ�lU���DcAb(�S�����הoF�a��!�U�D����,J@�����a�� ��6j0C��Qc#YYY!#XXX��F �d*(����E*�2AVB�E��)�U�H�&�LdXCI#XXX�����J�XQ,AIl����Yd92T�#XXX"��U�1J�[1"*,f�b"��K!,9h���!*T��	Hw�\����jA�:H��DH�O�����i���5����"�υ� ��_b'��4f�S�J��n�kn-�e�L���Tě&�4��,���6��<�>������g���NXT~t��xN�#!��s0�1�aZ��8�R���6�n�Ѣ��3�N� q{�z'c5�꒯C;�!���Nc�{SB8LVb�~�<���#-B��M��5��SWFL�b" �$L�2�JF������t�͛#YYY��VDOZE�iu���\�ԥ4��ϖ����tO�ڒm��w-�"�f*�G�є�'2<�'lI����v�� ��N�����5�p�d�F�+F2� �z�J���`�R!��+Xj��x�;d������>TOVdbO���Y��nC�jK@��B̓����x���� �#XXX�P$4@�Q��W�:~�7\c�z�N�$(�`��3�gѲ�}^���RnO���5�����<;��)�P�%	�1��`�N;~l3�Sq#YYY0�Q#��!��ŉ�U�u�J#8I���Z��t`�I�g���x�	�[�	��&8@f\���N&YXZ�5����p���#XXX#YYY6���;�˳Q�;��JLL��r�@�R�Ti�+M��%���Ɛ���l�n'h1��!~g!c�ЪZ�JknB�1=<�	�:��s(���,V�_�a)I��t�@���G#YYY�e�3��U�y�8�U��ҳ��X��<Ά�lC�5�0�n��8>15tU���ǖׄX���cm�ڤ4�N���1��d����3{��Y��!��Rȉ-���ˏ�#YYY�(��#XXXT��! �nK��K��i��ea{��Qu��w�.�z����6��8�n�\�M�N����e��bݜK��`�S �ސ::7W���,�a�yN���b����M4���K���'jsU��{�9��ee?w��@{v:P9J��^<���d��CL.��wt9�k.iq��9QN�d���4��9����vG	���u�&`�Р`�GD�S�c��#=;m�0�}ů�>,Ц�uI����S���'��#ǧ�;4��<t7Cw�e��j(���XC�*�����*gv`!��쏜�x�ry�XXhZM�x��Sݿ:~���]U��A=5*�\.Z'�7-[G$Q�UfZ�ː���h�{,��r�,n;`@|}�����Fwf;�c:8<�VfC��Mj��$i���KV��5�H�Z�>_L�V}��n�����46�G� �)k#YYY�MV�{ZQk��g#�>b[��#��p�o�����{{�����O�Y�R>���Ѳ*+�H_S�aP������Ǻ5>""r�iז'�Z�yU��7�lCÅ|b#XXX#Ad0<�c�>:��Y��#YYYs���g{f�ׯm)���� �e��5uj���R�e-dR}b��2I�HQ��R������kO6���qrf���#XXX	�І0m�0aE,څ0����%��|�G�8�;��ȋh�s��|��.rD8@xKH����v�!��#XXX�����@�d��B0��^�3F��4��хEU|c��^\x�쇯�ȝ���:����>;�����~3u���($��X��4`c�w���q~��j�1��_�GTq��y�g�Z�~���f���VݰS(±#YYY��Rl�C���t��쪙�;�����zt�Y������C��S%LC��_8�;���q�x��2�+����e���p�J���4�㫂��G�� ����Io+��i2ꭏ�7CqY$�ᶩZ*"i���L��#XXXA��&b�X�+ߦ.��&�)m)�]�o���ZGz5Jz���e�S����Iy�<BU;-#XXXt���|�#YYYT���\d.L�q���2�=6A���7�,Y��L������ǫli�Ҟ��Z��f�QY��	��]�^9��7��ź��~o��K�%y��3O;��!NH&^�#XXX�󳫝ڃ�F�p�����|�C�:!�5ݱ�-@�QdP�#YYYY22����(����d���!��v�aLAH�l�uT��#YYY��"�������Њu�|��`���#YYYP!�h�k-��l �X�$R*$��������k�ȞL��������z��u ��� �t��oե�g�Ab�ܽ����,m�_���vk��+�9�U�?80�"A�jV��߅����i���t���q�����b��m0�r�۫���:����I<�����Q��Z�������TGIaiT"��X)Y��66o���6�߿]�P!��5#YYY3]0��X��6Q��e�=��P�/�I�}z�"�!�$�w@�#XXX�)��wu�Pi%��N9 �np0�5=�վh�m��f���/���&�1��g�S�����:3����=�m�E�Ⱦ��3��#XXX��U	#YYY"%00E�Y#YYY� *|"i4�P�P�'��?y���9,�#YYYaB>Ј�Z�Hggm�>�t�,����������cv[��F���E ";�#XXX%�U���Q�A���s0��k`�q,�& �)!Y]]`ފ�4����'���=�9��Н b#XXX|XVy@��m�#XXX�`,�wG�zAB�r���gA�ds�Tlؙf�tO�Z�Bbd`�DE`�B#XXXA�t$1,����<�dPg����`bs�������op�g�~����^����	W�>J^$���l�$�ːszB�f)n��vմ���3�z�X+�c4uH�'�=n��ĉ�ܦhr����X����X������2�ĳ|�59�]��1#YYY�B��AHU��B@�׻s�4���}�Dr`��H�ݑ2���#![�b���	����I��sW�z^>�@�f;��F@���H	%}<E ��%,�/��	:1@�+����쓍�)Q�3�F��Gų�ETG�r���_�#XXX[�M퓫8�����|��t�$k���Mb��=����pl����6�<�U�A��y��u�2�ՂC�T#YYY��IT�Lj��)Jl�>ۉ�H���F��Kγ�Ǘ��������r`@�������k�W[ٻH��W�X�Oa,Pғ���.�JB���Fn�B�E�?�q�2&�+*�х����;�8B#YYY�����<�*�4���m�k����5�M�İ<�Sa1�C�#YYYf�.76[_�?kEV��v�4��cwV	M����qz��HH3�<�q�(��tB��/�Iz�n"�%��P�8&$�j:�X�Т�^*p�)��%<�pwMt�y���l��-C����ݵ��Q����#YYY�3��IH2<�F,Ď�4����6�|��e3�v�@���	��Ɂv�?F~�@���!�q|��5*k8��+����ǎ�^t�ix)j]'�鶥�G��%L�C�76���ԕG��#YYY+�8ݑ����ه����#�c��zY �IB#�1¾DѼp��Z�IjeRe4��d�dTUn��:�:�%�������:�������EЈ��! �C��zxu��Z(ULֲ.<����2?�4�(W�Ie���:޶ű�,�͜&V���f�W�g��S���W�����[�1�������H�#XXXD�
#<==
